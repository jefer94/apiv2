"""
Test cases for /user
"""
from django.urls.base import reverse_lazy
from rest_framework import status
from ..mixins import AuthTestCase


class AuthenticateTestSuite(AuthTestCase):
    """Authentication test suite"""
    def test_user_without_auth(self):
        """Test /user without auth"""
        url = reverse_lazy('authenticate:user')
        data = {'email': 'self@email.ok', 'password': 'self.password'}
        # return client.post(url, data)
        response = self.client.post(url, data)
        detail = str(response.data['detail'])
        status_code = int(response.data['status_code'])

        self.assertEqual(len(response.data), 2)
        self.assertEqual(detail, 'Authentication credentials were not provided.')
        self.assertEqual(status_code, 401)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user(self):
        """Test /user"""
        model = self.generate_models(authenticate=True)
        url = reverse_lazy('authenticate:user')

        response = self.client.get(url)
        json = response.json()

        self.assertEqual(json, [{
            'id': model.user.id,
            'email': model.user.email,
            'first_name': model.user.first_name,
            'last_name': model.user.last_name,
            'github': None,
            'profile': None,
        }])
