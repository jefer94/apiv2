# ModelsMixin

Provide one helper to transform models in one dictionary

```py
# models.py
from django.db import models


class City(models.Model):
    name = models.CharField(max_length=20)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)


# tests/urls/tests_endpoint.py
from rest_framework.test import APITestCase
from breathecode.tests.mixins import (
    GenerateModelsMixin,
    GenerateQueriesMixin,
    ModelsMixin
)


class TestSuite(APITestCase, GenerateModelsMixin, GenerateQueriesMixin, ModelsMixin):
    def setUp():
        self.generate_queries()

    """
    🔽🔽🔽 Parse one model to dict
    """
    def test_model_to_dict__one_model():
        city_kwargs = {'name': 'Fólkvangr'}
        model = self.generate_models(city=True, city_kwargs=city_kwargs)

        # our model is parsed to dictionary, without created_at and updated_at
        # properties, it get as first param our dictionary of models and as
        # second param the model name
        self.assertEqual(self.model_to_dict(model, 'city'), {
            'name': 'Fólkvangr',
        })

        # we can check if the data in db still without changes
        self.assertEqual(self.all_city_dict(), [{
            **self.model_to_dict(model, 'city')
        }])

    """
    🔽🔽🔽 Parse one list of models to dict with model_to_dict
    """
    def test_model_to_dict__one_list_of_models():
        # we generate a list of three models
        models = [self.generate_models(city=True) for _ in range(0, 3)]

        # we can check if the data in db still without changes
        self.assertEqual(self.all_city_dict(), [{
            **self.model_to_dict(model, 'city')
        } for model in models])

    """
    🔽🔽🔽 Parse one list of models to dict with all_model_dict
    """
    def test_all_model_dict__one_list_of_models():
        # we generate a list of three models
        models = [
            self.generate_models(city=True, city_kwargs={'name': 'Fólkvangr'}),
            self.generate_models(city=True, city_kwargs={'name': 'Valhalla'}),
            self.generate_models(city=True, city_kwargs={'name': 'Hades'}),
        ]

        # our list of models is parsed to one list of dictionaries, without
        # created_at and updated_at properties, get as first param the list
        # of models
        self.assertEqual(self.all_model_dict(models), [{
            'name': 'Fólkvangr',
        }, {
            'name': 'Valhalla',
        }, {
            'name': 'Hades',
        }])

        # we can check if the data in db still without changes
        self.assertEqual(self.all_city_dict(), self.all_model_dict(models))

    """
    🔽🔽🔽 Print one model
    """
    def test_print_model():
        # we generate one dictionary of models
        model = self.generate_models(city=True)

        # it print in terminal all attributes of model city like one dictionary
        self.print_model(model, 'city')

     """
    🔽🔽🔽 Print all models
    """
    def test_print_all_models():
        # we generate one dictionary of models
        model = self.generate_models(city=True)

        # it print in terminal all attributes of models like one dictionary
        self.print_all_models(models, 'city')
```
