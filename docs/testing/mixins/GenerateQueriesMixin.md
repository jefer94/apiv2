# GenerateQueriesMixin

Provide one helper to generate queries methods

```py
# models.py
from django.db import models


class City(models.Model):
    name = models.CharField(max_length=20)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)


class People(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)


# tests/urls/tests_endpoint.py
from rest_framework.test import APITestCase
from breathecode.tests.mixins import GenerateQueriesMixin


class TestSuite(APITestCase, GenerateQueriesMixin):
    """
    🔽🔽🔽 Get one model
    """
    def test_generate_queries__get_one_model():
        # currently self instance not have one get_city method
        self.assertFalse(hasattr(self, 'get_city'))

        # currently self instance not have one get_people method
        self.assertFalse(hasattr(self, 'get_people'))

        # generate queries method, it generally is in setUp method
        self.generate_queries()

        # currently self instance have one get_city method
        self.assertTrue(hasattr(self, 'get_city'))

        # currently self instance have one get_people method
        self.assertTrue(hasattr(self, 'get_people'))

        # it should return one instance of model city or None, get as parameter
        # the pk of model
        self.assertTrue(isinstance(self.get_city(1), City))

        # it should return one instance of model people or None, get as parameter
        # the pk of model
        self.assertTrue(isinstance(self.get_people(1), People))

    """
    🔽🔽🔽 Get one model in dictionary format
    """
    def test_generate_queries__get_one_model_in_dictionary_format():
        # currently self instance not have one get_city_dict method
        self.assertFalse(hasattr(self, 'get_city_dict'))

        # currently self instance not have one get_people_dict method
        self.assertFalse(hasattr(self, 'get_people_dict'))

        # generate queries method, it generally is in setUp method
        self.generate_queries()

        # currently self instance have one get_city_dict method
        self.assertTrue(hasattr(self, 'get_city_dict'))

        # currently self instance have one get_people_dict method
        self.assertTrue(hasattr(self, 'get_people_dict'))

        # it should return one dictionary city model attrs or None, get as parameter
        # the pk of model, some dinamics fields like created_at and updated_at
        # are deleted
        self.assertEqual(self.get_city_dict(1), {
            'name': 'Fólkvangr'
        })

        # it should return one instance of model people or None, get as parameter
        # the pk of model, some dinamics fields like created_at and updated_at
        # are deleted
        self.assertEqual(self.get_people_dict(1), {
            'first_name': 'Freyja',
            'last_name': 'Fólkvangr'
        })

    """
    🔽🔽🔽 Get one list of models
    """
    def test_generate_queries__get_one_list_of_models():
        # currently self instance not have one all_city method
        self.assertFalse(hasattr(self, 'all_city'))

        # currently self instance not have one all_people method
        self.assertFalse(hasattr(self, 'all_people'))

        # generate queries method, it generally is in setUp method
        self.generate_queries()

        # currently self instance have one all_city method
        self.assertTrue(hasattr(self, 'all_city'))

        # currently self instance have one all_people method
        self.assertTrue(hasattr(self, 'all_people'))

        # it should return one list of instances of models city
        self.assertEqual(len(self.all_city()), 1)
        self.assertTrue(isinstance(self.all_city()[0], City))

        # it should return one list of instances of model people
        self.assertEqual(len(self.all_people()), 1)
        self.assertTrue(isinstance(self.all_people()[0], People))

    """
    🔽🔽🔽 Get one list of models in dictionary format
    """
    def test_generate_queries__get_one_list_of_models_in_dictionary_format():
        # currently self instance not have one all_city_dict method
        self.assertFalse(hasattr(self, 'all_city_dict'))

        # currently self instance not have one all_people_dict method
        self.assertFalse(hasattr(self, 'all_people_dict'))

        # generate queries method, it generally is in setUp method
        self.generate_queries()

        # currently self instance have one all_city_dict method
        self.assertTrue(hasattr(self, 'all_city_dict'))

        # currently self instance have one all_people_dict method
        self.assertTrue(hasattr(self, 'all_people_dict'))

        # it should return one list of dictionaries of city model attrs, some
        # dinamics fields like created_at and updated_at are deleted
        self.assertEqual(self.all_city_dict(), [{
            'name': 'Fólkvangr'
        }])

        # it should return one list of dictionaries of people model attrs, some
        # dinamics fields like created_at and updated_at are deleted
        self.assertEqual(self.all_people_dict(), [{
            'first_name': 'Freyja',
            'last_name': 'Fólkvangr'
        }])
```
