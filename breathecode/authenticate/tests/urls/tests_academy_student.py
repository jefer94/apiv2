"""
Test cases for /academy/student
"""
from breathecode.services import datetime_to_iso_format
from django.urls.base import reverse_lazy
from rest_framework import status
from random import choice
from ...models import ProfileAcademy
from ..mixins.new_auth_test_case import AuthTestCase

# TODO: this test is incompleted
class AuthenticateTestSuite(AuthTestCase):

    """
    🔽🔽🔽 Auth
    """
    def test_academy_student__without_auth(self):
        """Test /academy/student without auth"""
        url = reverse_lazy('authenticate:academy_student')
        response = self.client.get(url)
        json = response.json()

        self.assertEqual(json, {
            'detail': 'Authentication credentials were not provided.',
            'status_code': status.HTTP_401_UNAUTHORIZED,
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_academy_student__without_capability(self):
        """Test /academy/student"""
        self.headers(academy=1)
        self.generate_models(authenticate=True)
        url = reverse_lazy('authenticate:academy_student')
        response = self.client.get(url)
        json = response.json()

        self.assertEqual(json, {
            'detail': "You (user: 1) don't have this capability: read_student "
                "for academy 1",
            'status_code': 403
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_academy_student__without_academy(self):
        """Test /academy/student"""
        self.headers(academy=1)
        role = 'konan'
        self.generate_models(authenticate=True, role=role,
            capability='read_student')
        url = reverse_lazy('authenticate:academy_student')
        response = self.client.get(url)
        json = response.json()

        self.assertEqual(json, {
            'detail': "You (user: 1) don't have this capability: read_student "
                "for academy 1",
            'status_code': 403
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    """
    🔽🔽🔽 Without data
    """
    def test_academy_student__without_student(self):
        """Test /academy/student"""
        self.headers(academy=1)
        role = 'konan'
        model = self.generate_models(authenticate=True, role=role,
            capability='read_student', profile_academy=True)
        url = reverse_lazy('authenticate:academy_student')
        response = self.client.get(url)
        json = response.json()

        self.assertEqual(json, [])
        self.assertEqual(self.all_profile_academy_dict(), [{
            'academy_id': 1,
            'address': None,
            'email': None,
            'first_name': None,
            'id': 1,
            'last_name': None,
            'phone': '',
            'role_id': 'konan',
            'status': 'INVITED',
            'user_id': 1
        }])

    """
    🔽🔽🔽 With data
    """
    def test_academy_student(self):
        """Test /academy/student"""
        self.headers(academy=1)
        role = 'student'
        model = self.generate_models(authenticate=True, role=role,
            capability='read_student', profile_academy=True)
        url = reverse_lazy('authenticate:academy_student')
        response = self.client.get(url)
        json = response.json()
        expected = [{
            'academy': {
                'id': model['profile_academy'].academy.id,
                'name': model['profile_academy'].academy.name,
                'slug': model['profile_academy'].academy.slug
            },
            'address': model['profile_academy'].address,
            'created_at': self.datetime_to_iso(model['profile_academy'].created_at),
            'email': model['profile_academy'].email,
            'first_name': model['profile_academy'].first_name,
            'id': model['profile_academy'].id,
            'last_name': model['profile_academy'].last_name,
            'phone': model['profile_academy'].phone,
            'role': {
                'name': 'student',
                'slug': 'student'
            },
            'status': 'INVITED',
            'user': {
                'email': model['profile_academy'].user.email,
                'first_name': model['profile_academy'].user.first_name,
                'github': None,
                'id': model['profile_academy'].user.id,
                'last_name': model['profile_academy'].user.last_name
            }
        }]

        self.assertEqual(json, expected)
        self.assertEqual(self.all_profile_academy_dict(), [{
            'academy_id': 1,
            'address': None,
            'email': None,
            'first_name': None,
            'id': 1,
            'last_name': None,
            'phone': '',
            'role_id': 'student',
            'status': 'INVITED',
            'user_id': 1
        }])

    """
    🔽🔽🔽 Pagination
    """
    def test_academy_student__pagination__with_105(self):
        """Test /academy/student"""
        self.headers(academy=1)
        role = 'student'
        model = self.generate_models(authenticate=True, role=role,
            capability='read_student', profile_academy=True)

        base = model.copy()
        del base['user']
        del base['profile_academy']

        models = [model] + [self.generate_models(profile_academy=True, models=base)
            for _ in range(0, 105)]
        url = reverse_lazy('authenticate:academy_student')
        response = self.client.get(url)
        json = response.json()
        expected = [{
            'academy': {
                'id': model['profile_academy'].academy.id,
                'name': model['profile_academy'].academy.name,
                'slug': model['profile_academy'].academy.slug
            },
            'address': model['profile_academy'].address,
            'created_at': self.datetime_to_iso(model['profile_academy'].created_at),
            'email': model['profile_academy'].email,
            'first_name': model['profile_academy'].first_name,
            'id': model['profile_academy'].id,
            'last_name': model['profile_academy'].last_name,
            'phone': model['profile_academy'].phone,
            'role': {
                'name': 'student',
                'slug': 'student'
            },
            'status': 'INVITED',
            'user': {
                'email': model['profile_academy'].user.email,
                'first_name': model['profile_academy'].user.first_name,
                'github': None,
                'id': model['profile_academy'].user.id,
                'last_name': model['profile_academy'].user.last_name
            }
        } for model in models if model['profile_academy'].id < 101]

        self.assertEqual(json, expected)
        self.assertEqual(self.all_profile_academy_dict(), [{
            'academy_id': 1,
            'address': None,
            'email': None,
            'first_name': None,
            'id': model['profile_academy'].id,
            'last_name': None,
            'phone': '',
            'role_id': 'student',
            'status': 'INVITED',
            'user_id': model['user'].id
        } for model in models])

    def test_academy_student__pagination__first_five(self):
        """Test /academy/student"""
        self.headers(academy=1)
        role = 'student'
        model = self.generate_models(authenticate=True, role=role,
            capability='read_student', profile_academy=True)

        base = model.copy()
        del base['user']
        del base['profile_academy']

        models = [model] + [self.generate_models(profile_academy=True, models=base)
            for _ in range(0, 9)]
        url = reverse_lazy('authenticate:academy_student') + '?limit=5&offset=0'
        response = self.client.get(url)
        json = response.json()
        expected = {
            'count': 10,
            'first': None,
            'last': 'http://testserver/v1/auth/academy/student?limit=5&offset=5',
            'next': 'http://testserver/v1/auth/academy/student?limit=5&offset=5',
            'previous': None,
            'results': [{
                'academy': {
                    'id': model['profile_academy'].academy.id,
                    'name': model['profile_academy'].academy.name,
                    'slug': model['profile_academy'].academy.slug
                },
                'address': model['profile_academy'].address,
                'created_at': self.datetime_to_iso(model['profile_academy'].created_at),
                'email': model['profile_academy'].email,
                'first_name': model['profile_academy'].first_name,
                'id': model['profile_academy'].id,
                'last_name': model['profile_academy'].last_name,
                'phone': model['profile_academy'].phone,
                'role': {
                    'name': 'student',
                    'slug': 'student'
                },
                'status': 'INVITED',
                'user': {
                    'email': model['profile_academy'].user.email,
                    'first_name': model['profile_academy'].user.first_name,
                    'github': None,
                    'id': model['profile_academy'].user.id,
                    'last_name': model['profile_academy'].user.last_name
                }
            } for model in models if model['profile_academy'].id < 6]
        }

        self.assertEqual(json, expected)
        self.assertEqual(self.all_profile_academy_dict(), [{
            'academy_id': 1,
            'address': None,
            'email': None,
            'first_name': None,
            'id': model['profile_academy'].id,
            'last_name': None,
            'phone': '',
            'role_id': 'student',
            'status': 'INVITED',
            'user_id': model['user'].id
        } for model in models])

    def test_academy_student__pagination__last_five(self):
        """Test /academy/student"""
        self.headers(academy=1)
        role = 'student'
        model = self.generate_models(authenticate=True, role=role,
            capability='read_student', profile_academy=True)

        base = model.copy()
        del base['user']
        del base['profile_academy']

        models = [model] + [self.generate_models(profile_academy=True, models=base)
            for _ in range(0, 9)]
        url = reverse_lazy('authenticate:academy_student') + '?limit=5&offset=5'
        response = self.client.get(url)
        json = response.json()
        expected = {
            'count': 10,
            'first': 'http://testserver/v1/auth/academy/student?limit=5',
            'last': None,
            'next': None,
            'previous': 'http://testserver/v1/auth/academy/student?limit=5',
            'results': [{
                'academy': {
                    'id': model['profile_academy'].academy.id,
                    'name': model['profile_academy'].academy.name,
                    'slug': model['profile_academy'].academy.slug
                },
                'address': model['profile_academy'].address,
                'created_at': self.datetime_to_iso(model['profile_academy'].created_at),
                'email': model['profile_academy'].email,
                'first_name': model['profile_academy'].first_name,
                'id': model['profile_academy'].id,
                'last_name': model['profile_academy'].last_name,
                'phone': model['profile_academy'].phone,
                'role': {
                    'name': 'student',
                    'slug': 'student'
                },
                'status': 'INVITED',
                'user': {
                    'email': model['profile_academy'].user.email,
                    'first_name': model['profile_academy'].user.first_name,
                    'github': None,
                    'id': model['profile_academy'].user.id,
                    'last_name': model['profile_academy'].user.last_name
                }
            } for model in models if model['profile_academy'].id > 5]
        }

        self.assertEqual(json, expected)
        self.assertEqual(self.all_profile_academy_dict(), [{
            'academy_id': 1,
            'address': None,
            'email': None,
            'first_name': None,
            'id': model['profile_academy'].id,
            'last_name': None,
            'phone': '',
            'role_id': 'student',
            'status': 'INVITED',
            'user_id': model['user'].id
        } for model in models])

    """
    🔽🔽🔽 Method delete without capability
    """
    def test_academy_student__delete__without_capability(self):
        """Test /cohort/:id/user without auth"""
        self.headers(academy=1)
        model = self.generate_models(authenticate=True)
        url = reverse_lazy('authenticate:academy_student')
        response = self.client.delete(url)
        json = response.json()
        expected = {
            'detail': "You (user: 1) don't have this capability: crud_student for academy 1",
            'status_code': 403
        }

        self.assertEqual(json, expected)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.all_profile_academy_dict(), [])

    """
    🔽🔽🔽 Delete without vars in querystring or bulk mode
    """
    def test_academy_student__delete__without_args_in_url_or_bulk(self):
        """Test /cohort/:id/user without auth"""
        self.headers(academy=1)
        model = self.generate_models(authenticate=True, profile_academy=True,
            capability='crud_student', role='student')
        url = reverse_lazy('authenticate:academy_student')
        response = self.client.delete(url)
        json = response.json()
        expected = {
            'details': "Missing user_id or academy_id",
            'status_code': 400
        }

        self.assertEqual(json, expected)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.all_profile_academy_dict(), [{
            **self.model_to_dict(model, 'profile_academy'),
        }])

    """
    🔽🔽🔽 Delete in bulk mode
    """
    def test_academy_student__delete__in_bulk__with_one(self):
        """Test /cohort/:id/user without auth"""
        self.headers(academy=1)
        many_fields = ['id']

        base = self.generate_models(academy=True, capability='crud_student', role='student')

        for field in many_fields:
            profile_academy_kwargs = {
                'email': choice(['a@a.com', 'b@b.com', 'c@c.com']),
                'first_name': choice(['Rene', 'Albert', 'Immanuel']),
                'last_name': choice(['Descartes', 'Camus', 'Kant']),
                'address': choice(['asd', 'qwe', 'zxc']),
                'phone': choice(['123', '456', '789']),
                'status': choice(['INVITED', 'ACTIVE']),
            }
            model = self.generate_models(authenticate=True, profile_academy=True,
                profile_academy_kwargs=profile_academy_kwargs, models=base)

            url = (reverse_lazy('authenticate:academy_student') + f'?{field}=' +
                str(getattr(model['profile_academy'], field)))
            response = self.client.delete(url)

            if response.status_code != 204:
                print(response.json())

            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            self.assertEqual(self.all_profile_academy_dict(), [])

    def test_academy_student__delete__in_bulk__with_two(self):
        """Test /cohort/:id/user without auth"""
        self.headers(academy=1)
        many_fields = ['id']

        base = self.generate_models(academy=True, capability='crud_student', role='student')

        for field in many_fields:
            profile_academy_kwargs = {
                'email': choice(['a@a.com', 'b@b.com', 'c@c.com']),
                'first_name': choice(['Rene', 'Albert', 'Immanuel']),
                'last_name': choice(['Descartes', 'Camus', 'Kant']),
                'address': choice(['asd', 'qwe', 'zxc']),
                'phone': choice(['123', '456', '789']),
                'status': choice(['INVITED', 'ACTIVE']),
            }
            model1 = self.generate_models(authenticate=True, profile_academy=True,
                profile_academy_kwargs=profile_academy_kwargs, models=base)

            profile_academy_kwargs = {
                'email': choice(['a@a.com', 'b@b.com', 'c@c.com']),
                'first_name': choice(['Rene', 'Albert', 'Immanuel']),
                'last_name': choice(['Descartes', 'Camus', 'Kant']),
                'address': choice(['asd', 'qwe', 'zxc']),
                'phone': choice(['123', '456', '789']),
                'status': choice(['INVITED', 'ACTIVE']),
            }
            model2 = self.generate_models(profile_academy=True,
                profile_academy_kwargs=profile_academy_kwargs, models=base)

            url = (reverse_lazy('authenticate:academy_student') + f'?{field}=' +
                str(getattr(model1['profile_academy'], field)) + ',' +
                str(getattr(model2['profile_academy'], field)))
            response = self.client.delete(url)

            if response.status_code != 204:
                print(response.json())

            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            self.assertEqual(self.all_profile_academy_dict(), [])

    """
    🔽🔽🔽 Delete in bulk mode just remove students
    """
    def test_academy_student__delete__in_bulk__with_two__but_is_not_student(self):
        """Test /cohort/:id/user without auth"""
        self.headers(academy=1)
        many_fields = ['id']

        base = self.generate_models(academy=True, capability='crud_student', role='hitman')

        for field in many_fields:
            profile_academy_kwargs = {
                'email': choice(['a@a.com', 'b@b.com', 'c@c.com']),
                'first_name': choice(['Rene', 'Albert', 'Immanuel']),
                'last_name': choice(['Descartes', 'Camus', 'Kant']),
                'address': choice(['asd', 'qwe', 'zxc']),
                'phone': choice(['123', '456', '789']),
                'status': choice(['INVITED', 'ACTIVE']),
            }
            model1 = self.generate_models(authenticate=True, profile_academy=True,
                profile_academy_kwargs=profile_academy_kwargs, models=base)

            profile_academy_kwargs = {
                'email': choice(['a@a.com', 'b@b.com', 'c@c.com']),
                'first_name': choice(['Rene', 'Albert', 'Immanuel']),
                'last_name': choice(['Descartes', 'Camus', 'Kant']),
                'address': choice(['asd', 'qwe', 'zxc']),
                'phone': choice(['123', '456', '789']),
                'status': choice(['INVITED', 'ACTIVE']),
            }
            model2 = self.generate_models(profile_academy=True,
                profile_academy_kwargs=profile_academy_kwargs, models=base)

            url = (reverse_lazy('authenticate:academy_student') + f'?{field}=' +
                str(getattr(model1['profile_academy'], field)) + ',' +
                str(getattr(model2['profile_academy'], field)))
            response = self.client.delete(url)

            if response.status_code != 204:
                print(response.json())

            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            self.assertEqual(self.all_profile_academy_dict(), [{
                **self.model_to_dict(model1, 'profile_academy'),
            }, {
                **self.model_to_dict(model2, 'profile_academy'),
            }])

            for model in ProfileAcademy.objects.all():
                model.delete()

    """
    🔽🔽🔽 Method post without capability
    """
    def test_academy_student__post__without_capability(self):
        """Test /cohort/:id/user without auth"""
        self.headers(academy=1)
        model = self.generate_models(authenticate=True)
        url = reverse_lazy('authenticate:academy_student')
        data = {}
        response = self.client.post(url, data)
        json = response.json()
        expected = {
            'detail': "You (user: 1) don't have this capability: crud_student for academy 1",
            'status_code': 403
        }

        self.assertEqual(json, expected)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.all_profile_academy_dict(), [])

    """
    🔽🔽🔽 Method post without user
    """
    def test_academy_student__post__without_user(self):
        """Test /cohort/:id/user without auth"""
        self.headers(academy=1)
        model = self.generate_models(authenticate=True, profile_academy=True,
            role='potato', capability='crud_student')
        url = reverse_lazy('authenticate:academy_student')
        data = {}
        response = self.client.post(url, data)
        json = response.json()
        expected = {
            'detail': 'user-not-exists',
            'status_code': 400
        }

        self.assertEqual(json, expected)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.all_profile_academy_dict(), [{
            **self.model_to_dict(model, 'profile_academy'),
        }])

    """
    🔽🔽🔽 Method post with user in the staff
    """
    def test_academy_student__post__with_user__with_profile_academy(self):
        """Test /cohort/:id/user without auth"""
        self.headers(academy=1)
        model = self.generate_models(authenticate=True, profile_academy=True,
            role='potato', capability='crud_student')
        url = reverse_lazy('authenticate:academy_student')
        data = {
            'user': model.user.id
        }
        response = self.client.post(url, data)
        json = response.json()
        expected = {
            'non_field_errors': ['This user is already a member of this academy staff']
        }

        self.assertEqual(json, expected)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.all_profile_academy_dict(), [{
            **self.model_to_dict(model, 'profile_academy'),
        }])

    """
    🔽🔽🔽 Method post with user, without role student
    """
    def test_academy_student__post__with_user__without_role_student(self):
        """Test /cohort/:id/user without auth"""
        self.headers(academy=1)
        base = self.generate_models(authenticate=True, profile_academy=True,
            role='potato', capability='crud_student')

        model = self.generate_models(user=True)
        url = reverse_lazy('authenticate:academy_student')
        data = {
            'user': model.user.id
        }
        response = self.client.post(url, data)
        json = response.json()
        expected = {'detail': 'role-student-not-found', 'status_code': 400}

        self.assertEqual(json, expected)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.all_profile_academy_dict(), [{
            **self.model_to_dict(base, 'profile_academy'),
        }])

    """
    🔽🔽🔽 Method post with user, without role student
    """
    def test_academy_student__post(self):
        """Test /cohort/:id/user without auth"""
        self.headers(academy=1)
        base = self.generate_models(authenticate=True, profile_academy=True,
            role='student', capability='crud_student')

        model = self.generate_models(user=True)
        url = reverse_lazy('authenticate:academy_student')
        data = {
            'user': model.user.id
        }
        response = self.client.post(url, data)
        json = response.json()
        expected = {'address': None,
            'email': model.user.email,
            'first_name': None,
            'last_name': None,
            'phone': '',
            'status': 'ACTIVE'
        }

        self.assertEqual(json, expected)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.all_profile_academy_dict(), [{
            **self.model_to_dict(base, 'profile_academy'),
        }, {
            'id': 2,
            'address': None,
            'academy_id': 1,
            'email': model.user.email,
            'first_name': None,
            'last_name': None,
            'phone': '',
            'role_id': 'student',
            'status': 'ACTIVE',
            'user_id': 2
        }])
