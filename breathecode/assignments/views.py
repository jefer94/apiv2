from typing_extensions import Self
from django.http import HttpResponseRedirect
from typing import Callable
from breathecode.authenticate.models import ProfileAcademy
import logging
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Q
from rest_framework.views import APIView
from django.contrib.auth.models import AnonymousUser
from django.contrib import messages
from breathecode.utils.api_view_extensions.api_view_extensions import APIViewExtensions
from breathecode.utils import ValidationException, capable_of, localize_query, GenerateLookupsMixin
from breathecode.admissions.models import Academy, CohortUser, Cohort
from breathecode.authenticate.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from breathecode.utils import APIException
from .models import Task, FinalProject
from .actions import deliver_task
from .caches import TaskCache
from .forms import DeliverAssigntmentForm
from .serializers import (TaskGETSerializer, PUTTaskSerializer, PostTaskSerializer, TaskGETDeliverSerializer,
                          FinalProjectGETSerializer, PostFinalProjectSerializer, PUTFinalProjectSerializer)
from .actions import sync_cohort_tasks
import breathecode.assignments.tasks as tasks
from django.db.models import QuerySet

logger = logging.getLogger(__name__)


class GenericTaskView(APIView):
    """
    This generic task view contains contents will be shared between the children
    """
    extensions = APIViewExtensions(cache=TaskCache, sort='-created_at', paginate=True)
    role = None

    def _get_roles(self, academy_id):
        return list(
            ProfileAcademy.objects.filter(academy__id=academy_id, user=self.request.user,
                                          status='ACTIVE').values_list('role__slug', flat=True))

    def _has_permission(self, user_roles, required_roles):
        for role in user_roles:
            if role in required_roles:
                return

        raise ValidationException('You not have the permissions to use this endpoint',
                                  slug='without-profile-academy')

    def _has_less_one_role(self, user_roles, required_roles) -> bool:
        for role in user_roles:
            if role in required_roles:
                return True

        return False

    def _apply_filters(self, items: QuerySet[Task], roles: list[str] = []) -> QuerySet[Task]:
        is_teacher = self._has_less_one_role(roles, ['TEACHER', 'ASSISTANT', 'REVIEWER'])

        if academy := self.request.GET.get('academy'):
            pks = academy.split(',')
            ids = [int(x) for x in pks if x.isnumeric()]
            slugs = [x for x in pks if not x.isnumeric()]
            items = items.filter(
                Q(cohort__academy__slug__in=slugs) | Q(cohort__academy__id__in=ids) | Q(cohort__isnull=True))

        if is_teacher and (user := self.request.GET.get('user')):
            items = items.filter(user__id__in=user.split(','))

        # tasks these cohorts (not the users, but the tasks belong to the cohort)
        if is_teacher and (cohort := self.request.GET.get('cohort')):
            cohorts = cohort.split(',')
            ids = [x for x in cohorts if x.isnumeric()]
            slugs = [x for x in cohorts if not x.isnumeric()]
            items = items.filter(Q(cohort__slug__in=slugs) | Q(cohort__id__in=ids))

        # tasks from users that belong to these cohort
        if cohort := self.request.GET.get('cohort'):
            if cohort == 'null':
                items = items.filter(cohort__isnull=True)

            else:
                ids = cohort.split(',')
                stu_cohorts = cohort.split(',')
                ids = [x for x in stu_cohorts if x.isnumeric()]
                slugs = [x for x in stu_cohorts if not x.isnumeric()]

                items = items.filter(
                    Q(user__cohortuser__cohort__id__in=ids) | Q(user__cohortuser__cohort__slug__in=slugs),
                    user__cohortuser__role='STUDENT',
                )

        if is_teacher and (edu_status := self.request.GET.get('edu_status')):
            items = items.filter(user__cohortuser__educational_status__in=edu_status.split(','))

        # tasks from users that belong to these cohort
        if is_teacher and (teacher := self.request.GET.get('teacher', None)):
            teacher_cohorts = CohortUser.objects.filter(user__id__in=teacher.split(','),
                                                        role='TEACHER').values_list('cohort__id', flat=True)
            items = items.filter(user__cohortuser__cohort__id__in=teacher_cohorts,
                                 user__cohortuser__role='STUDENT').distinct()

        if task_status := self.request.GET.get('task_status'):
            items = items.filter(task_status__in=task_status.split(','))

        if revision_status := self.request.GET.get('revision_status'):
            items = items.filter(revision_status__in=revision_status.split(','))

        if task_type := self.request.GET.get('task_type'):
            items = items.filter(task_type__in=task_type.split(','))

        return items

    def generic_get(self, initial_queryset: Callable[[], QuerySet[Task]], roles=[], academy_id=None):
        handler = self.extensions(self.request)
        cache = handler.cache.get()
        if cache is not None:
            return Response(cache, status=status.HTTP_200_OK)

        items = initial_queryset()

        user_roles = []

        if academy_id:
            user_roles = self._get_roles(academy_id)
            self._has_permission(user_roles, roles)

        items = self._apply_filters(items, user_roles)
        items = handler.queryset(items)

        serializer = TaskGETSerializer(items, many=True)
        return handler.response(serializer.data)

    def generic_get_by_id(self, task_id, user_id):
        handler = self.extensions(self.request)
        cache = handler.cache.get()
        if cache is not None:
            return Response(cache, status=status.HTTP_200_OK)

        if task_id is not None:
            item = Task.objects.filter(id=task_id, user__id=user_id).first()
            if item is None:
                raise ValidationException('Task not found', code=404, slug='task-not-found')

            serializer = TaskGETSerializer(item, many=False)
            return Response(serializer.data)


class TaskTeacherView(GenericTaskView):
    @capable_of('review_task')
    def get(self, _, academy_id=None):
        def initial_queryset():
            """Keep this function distinct to prevent use the database if exists elements in the cache"""

            return Task.objects.filter(Q(cohort__academy__id=academy_id) | Q(cohort__isnull=True))

        roles = ['TEACHER', 'ASSISTANT', 'REVIEWER']
        return self.generic_get(initial_queryset, roles, academy_id)


@api_view(['POST'])
def sync_cohort_tasks_view(request, cohort_id=None):
    item = Cohort.objects.filter(id=cohort_id).first()
    if item is None:
        raise ValidationException('Cohort not found')

    syncronized = sync_cohort_tasks(item)
    if len(syncronized) == 0:
        raise ValidationException('No tasks updated')

    serializer = TaskGETSerializer(syncronized, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class FinalProjectMeView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, project_id=None, user_id=None):
        if not user_id:
            user_id = request.user.id

        if project_id is not None:
            item = FinalProject.objects.filter(id=project_id, user__id=user_id).first()
            if item is None:
                raise ValidationException('Project not found', code=404, slug='project-not-found')

            serializer = FinalProjectGETSerializer(item, many=False)
            return Response(serializer.data)

        items = FinalProject.objects.filter(members__id=user_id)

        project_status = request.GET.get('project_status', None)
        if project_status is not None:
            items = items.filter(project_status__in=project_status.split(','))

        members = request.GET.get('members', None)
        if members is not None and isinstance(members, list):
            items = items.filter(members__id__in=members)

        revision_status = request.GET.get('revision_status', None)
        if revision_status is not None:
            items = items.filter(revision_status__in=revision_status.split(','))

        visibility_status = request.GET.get('visibility_status', None)
        if visibility_status is not None:
            items = items.filter(visibility_status__in=visibility_status.split(','))
        else:
            items = items.filter(visibility_status='PUBLIC')

        cohort = request.GET.get('cohort', None)
        if cohort is not None:
            if cohort == 'null':
                items = items.filter(cohort__isnull=True)
            else:
                cohorts = cohort.split(',')
                ids = [x for x in cohorts if x.isnumeric()]
                slugs = [x for x in cohorts if not x.isnumeric()]
                items = items.filter(Q(cohort__slug__in=slugs) | Q(cohort__id__in=ids))

        serializer = FinalProjectGETSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request, user_id=None):

        # only create tasks for yourself
        if user_id is None:
            user_id = request.user.id

        payload = request.data

        if isinstance(request.data, list) == False:
            payload = [request.data]

        serializer = PostFinalProjectSerializer(data=payload,
                                                context={
                                                    'request': request,
                                                    'user_id': user_id
                                                },
                                                many=True)
        if serializer.is_valid():
            serializer.save()
            # tasks.teacher_task_notification.delay(serializer.data['id'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, project_id=None):
        def update(_req, data, _id=None, only_validate=True):
            if _id is None:
                raise ValidationException('Missing project id to update', slug='missing-project-id')

            item = FinalProject.objects.filter(id=_id).first()
            if item is None:
                raise ValidationException('Final Project not found', slug='project-not-found')

            serializer = PUTFinalProjectSerializer(item, data=data, context={'request': _req})
            if serializer.is_valid():
                if not only_validate:
                    serializer.save()
                return status.HTTP_200_OK, serializer.data
            return status.HTTP_400_BAD_REQUEST, serializer.errors

        if project_id is not None:
            code, data = update(request, request.data, project_id, only_validate=False)
            return Response(data, status=code)

        else:  # project_id is None:

            if isinstance(request.data, list) == False:
                raise ValidationException(
                    'You are trying to update many project at once but you didn\'t provide a list on the payload',
                    slug='update-without-list')

            for item in request.data:
                if 'id' not in item:
                    item['id'] = None
                code, data = update(request, item, item['id'], only_validate=True)
                if code != status.HTTP_200_OK:
                    return Response(data, status=code)

            updated_projects = []
            for item in request.data:
                code, data = update(request, item, item['id'], only_validate=False)
                if code == status.HTTP_200_OK:
                    updated_projects.append(data)

            return Response(updated_projects, status=status.HTTP_200_OK)


class CohortTaskView(APIView, GenerateLookupsMixin):
    """
    List all snippets, or create a new snippet.
    """
    extensions = APIViewExtensions(cache=TaskCache, sort='-created_at', paginate=True)

    @capable_of('read_assignment')
    def get(self, request, cohort_id, academy_id):
        handler = self.extensions(request)
        cache = handler.cache.get()
        if cache is not None:
            return Response(cache, status=status.HTTP_200_OK)

        items = Task.objects.all()
        lookup = {}

        if isinstance(cohort_id, int) or cohort_id.isnumeric():
            lookup['cohort__id'] = cohort_id
        else:
            lookup['cohort__slug'] = cohort_id

        task_type = request.GET.get('task_type', None)
        if task_type is not None:
            lookup['task_type__in'] = task_type.split(',')

        task_status = request.GET.get('task_status', None)
        if task_status is not None:
            lookup['task_status__in'] = task_status.split(',')

        revision_status = request.GET.get('revision_status', None)
        if revision_status is not None:
            lookup['revision_status__in'] = revision_status.split(',')

        like = request.GET.get('like', None)
        if like is not None and like != 'undefined' and like != '':
            items = items.filter(Q(associated_slug__icontains=like) | Q(title__icontains=like))

        # tasks from users that belong to these cohort
        student = request.GET.get('student', None)
        if student is not None:
            lookup['user__cohortuser__user__id__in'] = student.split(',')
            lookup['user__cohortuser__role'] = 'STUDENT'

        items = items.filter(**lookup)
        items = handler.queryset(items)

        serializer = TaskGETSerializer(items, many=True)
        return handler.response(serializer.data)


class AcademyTaskView(GenericTaskView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, _, task_id=None, user_id=None):
        def initial_queryset():
            """Keep this function distinct to prevent use the database if exists elements in the cache"""

            lookup = {}

            if task_id:
                lookup['task__id'] = task_id

            if task_id:
                lookup['user__id'] = user_id

            return Task.objects.filter(**lookup)

        if task_id:
            return self.generic_get_by_id(task_id, user_id)

        roles = []
        return self.generic_get(initial_queryset, roles)


class TaskMeView(GenericTaskView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, task_id=None):
        def initial_queryset():
            """Keep this function distinct to prevent use the database if exists elements in the cache"""

            return Task.objects.filter(user__id=request.user.id)

        if task_id:
            return self.generic_get_by_id(task_id, request.user.id)

        roles = []
        return self.generic_get(initial_queryset, roles)

    def put(self, request, task_id=None):
        def update(_req, data, _id=None, only_validate=True):
            if _id is None:
                raise ValidationException('Missing task id to update', slug='missing=task-id')

            item = Task.objects.filter(id=_id).first()
            if item is None:
                raise ValidationException('Task not found', slug='task-not-found')
            serializer = PUTTaskSerializer(item, data=data, context={'request': _req})
            if serializer.is_valid():
                if not only_validate:
                    serializer.save()
                    if _req.user.id != item.user.id:
                        tasks.student_task_notification.delay(item.id)
                return status.HTTP_200_OK, serializer.data
            return status.HTTP_400_BAD_REQUEST, serializer.errors

        if task_id is not None:
            code, data = update(request, request.data, task_id, only_validate=False)
            return Response(data, status=code)

        else:  # task_id is None:

            if isinstance(request.data, list) == False:
                raise ValidationException(
                    'You are trying to update many tasks at once but you didn\'t provide a list on the payload',
                    slug='update-whout-list')

            for item in request.data:
                if 'id' not in item:
                    item['id'] = None
                code, data = update(request, item, item['id'], only_validate=True)
                if code != status.HTTP_200_OK:
                    return Response(data, status=code)

            updated_tasks = []
            for item in request.data:
                code, data = update(request, item, item['id'], only_validate=False)
                if code == status.HTTP_200_OK:
                    updated_tasks.append(data)

            return Response(updated_tasks, status=status.HTTP_200_OK)

    def post(self, request):
        # only create tasks for yourself
        user_id = request.user.id
        payload = request.data

        if isinstance(request.data, list) == False:
            payload = [request.data]

        serializer = PostTaskSerializer(data=payload,
                                        context={
                                            'request': request,
                                            'user_id': user_id
                                        },
                                        many=True)
        if serializer.is_valid():
            serializer.save()
            # tasks.teacher_task_notification.delay(serializer.data['id'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, task_id=None):

        if task_id is not None:
            item = Task.objects.filter(id=task_id, user__id=request.user.id).first()
            if item is None:
                raise ValidationException('Task not found for this user', slug='task-not-found')

            item.delete()

        else:  # task_id is None:
            ids = request.GET.get('id', '')
            if ids == '':
                raise ValidationException('Missing querystring propery id for bulk delete tasks',
                                          slug='missing-id')
            ids_to_delete = [id.strip() for id in ids.split(',')]
            Task.objects.filter(id__in=ids_to_delete, user__id=request.user.id).delete()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


class TaskMeDeliverView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    @capable_of('task_delivery_details')
    def get(self, request, task_id, academy_id):

        item = Task.objects.filter(id=task_id).first()
        if item is None:
            raise ValidationException('Task not found')

        serializer = TaskGETDeliverSerializer(item, many=False)
        return Response(serializer.data)


def deliver_assignment_view(request, task_id, token):

    if request.method == 'POST':
        _dict = request.POST.copy()
        form = DeliverAssigntmentForm(_dict)

        if 'github_url' not in _dict or _dict['github_url'] == '':
            messages.error(request, 'Github URL is required')
            return render(request, 'form.html', {'form': form})

        token = Token.objects.filter(key=_dict['token']).first()
        if token is None or token.expires_at < timezone.now():
            messages.error(request, f'Invalid or expired deliver token {_dict["token"]}')
            return render(request, 'form.html', {'form': form})

        task = Task.objects.filter(id=_dict['task_id']).first()
        if task is None:
            messages.error(request, 'Invalid task id')
            return render(request, 'form.html', {'form': form})

        deliver_task(
            task=task,
            github_url=_dict['github_url'],
            live_url=_dict['live_url'],
        )

        if 'callback' in _dict and _dict['callback'] != '':
            return HttpResponseRedirect(redirect_to=_dict['callback'] + '?msg=The task has been delivered')
        else:
            return render(request, 'message.html', {'message': 'The task has been delivered'})
    else:
        task = Task.objects.filter(id=task_id).first()
        if task is None:
            return render(request, 'message.html', {
                'message': f'Invalid assignment id {str(task_id)}',
            })

        _dict = request.GET.copy()
        _dict['callback'] = request.GET.get('callback', '')
        _dict['token'] = token
        _dict['task_name'] = task.title
        _dict['task_id'] = task.id
        form = DeliverAssigntmentForm(_dict)
    return render(
        request,
        'form.html',
        {
            'form': form,
            # 'heading': 'Deliver project assignment',
            'intro': 'Please fill the following information to deliver your assignment',
            'btn_lable': 'Deliver Assignment'
        })
