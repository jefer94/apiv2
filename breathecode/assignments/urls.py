from django.urls import path
from .views import (TaskMeView, AcademyTaskView, sync_cohort_tasks_view, deliver_assignment_view,
                    TaskDeliverView, FinalProjectMeView, CohortTaskView, AcademyFinalProjectView)

app_name = 'assignments'
urlpatterns = [
    path('user/me/task', TaskMeView.as_view(), name='user_me_task'),
    path('user/me/task/<int:task_id>', TaskMeView.as_view(), name='user_me_task_id'),
    path('user/me/final_project', FinalProjectMeView.as_view(), name='user_me_final_project'),
    path('user/me/final_project/<int:project_id>', FinalProjectMeView.as_view(), name='user_me_project'),
    path('cohort/<int:cohort_id>/task', CohortTaskView.as_view()),
    path('task', AcademyTaskView.as_view(), name='task'),
    path('task/<int:task_id>', AcademyTaskView.as_view(), name='task_id'),
    path('user/<int:user_id>/task', AcademyTaskView.as_view(), name='user_id_task'),
    path('user/<int:user_id>/task/<int:task_id>', AcademyTaskView.as_view(), name='user_id_task_id'),
    path('final_project', AcademyFinalProjectView.as_view(), name='final_project'),
    path('final_project/<int:task_id>', AcademyFinalProjectView.as_view(), name='final_project_id'),
    path('user/<int:user_id>/final_project', AcademyFinalProjectView.as_view(), name='user_id_final_project'),
    path('user/<int:user_id>/final_project/<int:task_id>',
         AcademyFinalProjectView.as_view(),
         name='user_id_final_project_id'),
    path('task/<int:task_id>/deliver/<str:token>', deliver_assignment_view, name='task_id_deliver_token'),
    path('task/<int:task_id>/deliver', TaskDeliverView.as_view(), name='task_id_deliver'),
    path('sync/cohort/<int:cohort_id>/task', sync_cohort_tasks_view, name='sync_cohort_id_task'),
]
