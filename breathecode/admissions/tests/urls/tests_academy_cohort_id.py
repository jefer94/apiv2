"""
Test /cohort
"""
import re
from unittest.mock import patch
from django.urls.base import reverse_lazy
from rest_framework import status
from breathecode.tests.mocks import (
    GOOGLE_CLOUD_PATH,
    apply_google_cloud_client_mock,
    apply_google_cloud_bucket_mock,
    apply_google_cloud_blob_mock,
)
from ..mixins.new_admissions_test_case import AdmissionsTestCase

class AcademyCohortTestSuite(AdmissionsTestCase):
    """Test /cohort"""

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_cohort_id_without_auth(self):
        """Test /cohort/:id without auth"""
        self.headers(academy=1)
        url = reverse_lazy('admissions:academy_cohort_id', kwargs={'cohort_id': 1})
        response = self.client.put(url, {})
        json = response.json()

        self.assertEqual(json, {
            'detail': 'Authentication credentials were not provided.',
            'status_code': status.HTTP_401_UNAUTHORIZED
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_cohort_id_put_without_capability(self):
        """Test /cohort/:id without auth"""
        self.headers(academy=1)
        url = reverse_lazy('admissions:academy_cohort_id', kwargs={'cohort_id': 1})
        self.generate_models(authenticate=True)
        data = {}
        response = self.client.put(url, data)
        json = response.json()

        self.assertEqual(json, {
            'detail': "You (user: 1) don't have this capability: crud_cohort for academy 1",
            'status_code': 403
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_cohort_id_put_without_cohort(self):
        """Test /cohort/:id without auth"""
        self.headers(academy=1)
        url = reverse_lazy('admissions:academy_cohort_id', kwargs={'cohort_id': 99999})
        model = self.generate_models(authenticate=True, profile_academy=True,
            capability='crud_cohort', role='potato', syllabus=True)
        data = {}
        response = self.client.put(url, data)
        json = response.json()

        self.assertEqual(json, {'status_code': 400, 'detail': 'Specified cohort not be found'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.count_cohort(), 1)
        self.assertEqual(self.get_cohort_dict(1), self.remove_dinamics_fields(model['cohort'].__dict__))

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_cohort_id_put(self):
        """Test /cohort/:id without auth"""
        self.headers(academy=1)
        url = reverse_lazy('admissions:academy_cohort_id', kwargs={'cohort_id': 1})
        model = self.generate_models(authenticate=True, profile_academy=True,
            capability='crud_cohort', role='potato')
        data = {}
        response = self.client.put(url, data)
        json = response.json()

        expected = {
            'id': model['cohort'].id,
            'slug': model['cohort'].slug,
            'name': model['cohort'].name,
            'kickoff_date': self.datetime_to_iso(model['cohort'].kickoff_date),
            'ending_date': model['cohort'].ending_date,
            'current_day': model['cohort'].current_day,
            'stage': model['cohort'].stage,
            'language': model['cohort'].language,
            'syllabus': None,
        }

        self.assertEqual(json, expected)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.all_cohort_dict(), [self.remove_dinamics_fields(model['cohort'].__dict__)])
        self.assertEqual(self.count_cohort(), 1)
        self.assertEqual(self.get_cohort_dict(1), self.remove_dinamics_fields(model['cohort'].__dict__))

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_cohort_id_put_with_id_with_bad_syllabus_version_malformed(self):
        """Test /cohort/:id without auth"""
        self.headers(academy=1)
        model = self.generate_models(authenticate=True, cohort=True, profile_academy=True,
            capability='crud_cohort', role='potato', syllabus=True)
        url = reverse_lazy('admissions:academy_cohort_id', kwargs={'cohort_id': model['cohort'].id})
        data = {
            'syllabus': 1,
            'slug': 'they-killed-kenny',
            'name': 'They killed kenny',
            'current_day': model['cohort'].current_day + 1,
            'language': 'es',
        }
        response = self.client.put(url, data)
        json = response.json()
        expected = {
            'non_field_errors': ['Syllabus field marformed(`${certificate.slug}'
                '.v{syllabus.version}`)']
        }

        self.assertEqual(json, expected)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.all_cohort_dict(), [{
            'academy_id': 1,
            'current_day': model['cohort'].current_day,
            'ending_date': model['cohort'].ending_date,
            'id': model['cohort'].id,
            'kickoff_date': model['cohort'].kickoff_date,
            'language': model['cohort'].language,
            'name': model['cohort'].name,
            'slug': model['cohort'].slug,
            'stage': model['cohort'].stage,
            'syllabus_id': model['cohort'].syllabus.id,
            'timezone': None,
        }])

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_cohort_id_put_with_id_with_bad_syllabus_version(self):
        """Test /cohort/:id without auth"""
        self.headers(academy=1)
        model = self.generate_models(authenticate=True, cohort=True, profile_academy=True,
            capability='crud_cohort', role='potato', syllabus=True)
        url = reverse_lazy('admissions:academy_cohort_id', kwargs={'cohort_id': model['cohort'].id})
        data = {
            'syllabus': 'they-killed-kenny.v1',
            'slug': 'they-killed-kenny',
            'name': 'They killed kenny',
            'current_day': model['cohort'].current_day + 1,
            'language': 'es',
        }
        response = self.client.put(url, data)
        json = response.json()
        expected = {
            'non_field_errors': ["Syllabus doesn't exist"]
        }

        self.assertEqual(json, expected)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.all_cohort_dict(), [{
            'academy_id': 1,
            'current_day': model['cohort'].current_day,
            'ending_date': model['cohort'].ending_date,
            'id': model['cohort'].id,
            'kickoff_date': model['cohort'].kickoff_date,
            'language': model['cohort'].language,
            'name': model['cohort'].name,
            'slug': model['cohort'].slug,
            'stage': model['cohort'].stage,
            'syllabus_id': model['cohort'].syllabus.id,
            'timezone': None,
        }])

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_cohort_id_put_with_id_with_bad_syllabus_version_with_bad_slug(self):
        """Test /cohort/:id without auth"""
        self.headers(academy=1)
        model = self.generate_models(authenticate=True, cohort=True, profile_academy=True,
            capability='crud_cohort', role='potato', syllabus=True)
        url = reverse_lazy('admissions:academy_cohort_id', kwargs={'cohort_id': model['cohort'].id})
        data = {
            'syllabus': 'they-killed-kenny.v' + str(model['syllabus'].version),
            'slug': 'they-killed-kenny',
            'name': 'They killed kenny',
            'current_day': model['cohort'].current_day + 1,
            'language': 'es',
        }
        response = self.client.put(url, data)
        json = response.json()
        expected = {
            'non_field_errors': ["Syllabus doesn't exist"]
        }

        self.assertEqual(json, expected)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.all_cohort_dict(), [{
            'academy_id': 1,
            'current_day': model['cohort'].current_day,
            'ending_date': model['cohort'].ending_date,
            'id': model['cohort'].id,
            'kickoff_date': model['cohort'].kickoff_date,
            'language': model['cohort'].language,
            'name': model['cohort'].name,
            'slug': model['cohort'].slug,
            'stage': model['cohort'].stage,
            'syllabus_id': model['cohort'].syllabus.id,
            'timezone': None,
        }])

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_cohort_id_put_with_id_with_bad_syllabus_version_with_bad_version(self):
        """Test /cohort/:id without auth"""
        self.headers(academy=1)
        model = self.generate_models(authenticate=True, cohort=True, profile_academy=True,
            capability='crud_cohort', role='potato', syllabus=True)
        url = reverse_lazy('admissions:academy_cohort_id', kwargs={'cohort_id': model['cohort'].id})
        data = {
            'syllabus': model['certificate'].slug + '.v1',
            'slug': 'they-killed-kenny',
            'name': 'They killed kenny',
            'current_day': model['cohort'].current_day + 1,
            'language': 'es',
        }
        response = self.client.put(url, data)
        json = response.json()
        expected = {
            'non_field_errors': ["Syllabus doesn't exist"]
        }

        self.assertEqual(json, expected)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.all_cohort_dict(), [{
            'academy_id': 1,
            'current_day': model['cohort'].current_day,
            'ending_date': model['cohort'].ending_date,
            'id': model['cohort'].id,
            'kickoff_date': model['cohort'].kickoff_date,
            'language': model['cohort'].language,
            'name': model['cohort'].name,
            'slug': model['cohort'].slug,
            'stage': model['cohort'].stage,
            'syllabus_id': model['cohort'].syllabus.id,
            'timezone': None,
        }])

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_cohort_id_put_with_id_with_data_in_body(self):
        """Test /cohort/:id without auth"""
        self.headers(academy=1)
        model = self.generate_models(authenticate=True, cohort=True, profile_academy=True,
            capability='crud_cohort', role='potato', syllabus=True)
        url = reverse_lazy('admissions:academy_cohort_id', kwargs={'cohort_id': model['cohort'].id})
        data = {
            'syllabus': model['certificate'].slug + '.v' + str(model['syllabus'].version),
            'slug': 'they-killed-kenny',
            'name': 'They killed kenny',
            'current_day': model['cohort'].current_day + 1,
            'language': 'es',
        }
        response = self.client.put(url, data)
        json = response.json()
        expected = {
            'id': model['cohort'].id,
            'slug': data['slug'],
            'name': data['name'],
            'kickoff_date': self.datetime_to_iso(model['cohort'].kickoff_date),
            'ending_date': model['cohort'].ending_date,
            'current_day': data['current_day'],
            'stage': model['cohort'].stage,
            'language': data['language'],
            'syllabus': model['cohort'].syllabus.certificate.slug + '.v' +
                str(model['cohort'].syllabus.version),
        }

        self.assertEqual(json, expected)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.all_cohort_dict(), [{
            'academy_id': 1,
            'current_day': data['current_day'],
            'ending_date': model['cohort'].ending_date,
            'id': model['cohort'].id,
            'kickoff_date': model['cohort'].kickoff_date,
            'language': data['language'],
            'name': data['name'],
            'slug': data['slug'],
            'stage': model['cohort'].stage,
            'syllabus_id': model['cohort'].syllabus.id,
            'timezone': None,
        }])

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_cohort_id_get_with_id(self):
        """Test /cohort/:id without auth"""
        self.headers(academy=1)
        model = self.generate_models(authenticate=True, cohort=True, profile_academy=True,
            capability='read_cohort', role='potato', syllabus=True)
        model_dict = self.remove_dinamics_fields(model['cohort'].__dict__)
        url = reverse_lazy('admissions:academy_cohort_id', kwargs={'cohort_id': model['cohort'].id})
        response = self.client.get(url)
        json = response.json()
        expected = {
            'id': model['cohort'].id,
            'slug': model['cohort'].slug,
            'name': model['cohort'].name,
            'kickoff_date': self.datetime_to_iso(model['cohort'].kickoff_date),
            'ending_date': model['cohort'].ending_date,
            'stage': model['cohort'].stage,
            'language': model['cohort'].language,
            'syllabus': {
                'certificate': {
                    'id': model['cohort'].syllabus.certificate.id,
                    'slug': model['cohort'].syllabus.certificate.slug,
                    'name': model['cohort'].syllabus.certificate.name,
                },
                'version': model['cohort'].syllabus.version,
            },
            'academy': {
                'id': model['cohort'].academy.id,
                'slug': model['cohort'].academy.slug,
                'name': model['cohort'].academy.name,
                'country': {
                    'code': model['cohort'].academy.country.code,
                    'name': model['cohort'].academy.country.name,
                },
                'city': {
                    'name': model['cohort'].academy.city.name,
                },
                'logo_url': model['cohort'].academy.logo_url,
            },
        }

        self.assertEqual(json, expected)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.count_cohort(), 1)
        self.assertEqual(self.get_cohort_dict(1), model_dict)

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_cohort_id_get_with_bad_slug(self):
        """Test /cohort/:id without auth"""
        self.headers(academy=1)
        self.generate_models(authenticate=True, cohort=True, profile_academy=True,
            capability='read_cohort', role='potato', syllabus=True)
        url = reverse_lazy('admissions:academy_cohort_id', kwargs={'cohort_id': 'they-killed-kenny'})
        response = self.client.get(url)

        self.assertEqual(response.data, None)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_cohort_id_get_with_slug(self):
        """Test /cohort/:id without auth"""
        self.headers(academy=1)
        model = self.generate_models(authenticate=True, cohort=True, profile_academy=True,
            capability='read_cohort', role='potato', syllabus=True)
        model_dict = self.remove_dinamics_fields(model['cohort'].__dict__)
        url = reverse_lazy('admissions:academy_cohort_id', kwargs={'cohort_id': model['cohort'].slug})
        response = self.client.get(url)
        json = response.json()
        expected = {
            'id': model['cohort'].id,
            'slug': model['cohort'].slug,
            'name': model['cohort'].name,
            'kickoff_date': self.datetime_to_iso(model['cohort'].kickoff_date),
            'ending_date': model['cohort'].ending_date,
            'language': model['cohort'].language,
            'stage': model['cohort'].stage,
            'syllabus': {
                'certificate': {
                    'id': model['cohort'].syllabus.certificate.id,
                    'slug': model['cohort'].syllabus.certificate.slug,
                    'name': model['cohort'].syllabus.certificate.name,
                },
                'version': model['cohort'].syllabus.version,
            },
            'academy': {
                'id': model['cohort'].academy.id,
                'slug': model['cohort'].academy.slug,
                'name': model['cohort'].academy.name,
                'country': model['cohort'].academy.country,
                'city': model['cohort'].academy.city,
                'logo_url': model['cohort'].academy.logo_url,
                'country': {
                    'code': model['cohort'].academy.country.code,
                    'name': model['cohort'].academy.country.name,
                },
                'city': {
                    'name': model['cohort'].academy.city.name,
                },
            },
        }

        self.assertEqual(json, expected)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.count_cohort(), 1)
        self.assertEqual(self.get_cohort_dict(1), model_dict)

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_cohort_id_delete_with_bad_id(self):
        """Test /cohort/:id without auth"""
        self.headers(academy=1)
        model = self.generate_models(authenticate=True, cohort=True, user=True, profile_academy=True,
            capability='read_cohort', role='potato', syllabus=True, cohort_user=True)
        url = reverse_lazy('admissions:academy_cohort_id', kwargs={'cohort_id': 0})
        self.assertEqual(self.count_cohort_user(), 1)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.count_cohort_user(), 1)
        self.assertEqual(self.count_cohort_stage(model['cohort'].id), 'INACTIVE')

    @patch(GOOGLE_CLOUD_PATH['client'], apply_google_cloud_client_mock())
    @patch(GOOGLE_CLOUD_PATH['bucket'], apply_google_cloud_bucket_mock())
    @patch(GOOGLE_CLOUD_PATH['blob'], apply_google_cloud_blob_mock())
    def test_cohort_id_delete_with_id(self):
        """Test /cohort/:id without auth"""
        self.headers(academy=1)
        model = self.generate_models(authenticate=True, cohort=True, user=True, profile_academy=True,
            capability='crud_cohort', role='potato', syllabus=True, cohort_user=True)
        url = reverse_lazy('admissions:academy_cohort_id', kwargs={'cohort_id': model['cohort'].id})
        self.assertEqual(self.count_cohort_user(), 1)
        self.assertEqual(self.count_cohort_stage(model['cohort'].id), 'INACTIVE')
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.count_cohort_user(), 0)
        self.assertEqual(self.count_cohort_stage(model['cohort'].id), 'DELETED')
