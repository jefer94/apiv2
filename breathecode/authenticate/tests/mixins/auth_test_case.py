"""
Collections of mixins used to login in authorize microservice
"""
from breathecode.authenticate.models import ProfileAcademy
from unittest.mock import patch
from django.contrib.auth.models import User
from django.urls.base import reverse_lazy
from rest_framework.test import APITestCase, APIClient
from mixer.backend.django import mixer
from django.core.cache import cache
from breathecode.tests.mixins import GenerateModelsMixin, CacheMixin, GenerateQueriesMixin, DatetimeMixin, ICallMixin
from breathecode.tests.mocks import (GOOGLE_CLOUD_PATH, apply_google_cloud_client_mock,
                                     apply_google_cloud_bucket_mock, apply_google_cloud_blob_mock)


class AuthTestCase(APITestCase, GenerateModelsMixin, CacheMixin, GenerateQueriesMixin, DatetimeMixin,
                   ICallMixin):
    """APITestCase with auth methods"""
    def setUp(self):
        self.generate_queries()

    def tearDown(self):
        self.clear_cache()

    def create_user(self, email='', password=''):
        """Get login response"""
        url = reverse_lazy('authenticate:login')
        data = {'email': email, 'password': password}
        return self.client.post(url, data)

    def login(self, email='', password=''):
        """Login"""
        response = self.create_user(email=email, password=password)

        if 'token' in response.data.keys():
            self.token = str(response.data['token'])
            self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

        return response
