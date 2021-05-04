# GenerateModelsMixin

Provide one helper to generate models

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
from breathecode.tests.mixins import GenerateModelsMixin


class TestSuite(APITestCase, GenerateModelsMixin):
    """
    🔽🔽🔽 Get credentials
    """
    def test_generate_models__get_credentials():
        # get credentials to the requests through of self.client.{method_name}
        # and generate one user
        model = self.generate_models(authenticate=True)

        # self.generate_models return one dictionary of models
        self.assertEqual(len(model), 1)

        # the django user used in the auth process is in models result
        self.assertTrue('user' in model)

    """
    🔽🔽🔽 Generate models with arguments
    """
    def test_generate_models__with_arguments():
        # optional arguments to model {model_name}, through of
        # {model_name}_kwargs
        people_kwargs = {'first_name': 'Freyja'}

        # optional arguments should be, one table name equal to True or one
        # table name ending in _kwargs equal to one dictionary, it's pass
        # directly to mixer as attribute of model
        model = self.generate_models(people=True, people_kwargs=people_kwargs)

        # self.generate_models return one dictionary of models
        self.assertEqual(len(model), 1)

        # self.generate_models return one dictionary of models, we should
        # get the model with dict or list syntaxt
        self.assertTrue(isinstance(model['people'], People))

        # self.generate_models return one dictionary of models, we should
        # get the model with class attribute or javascript object syntaxt
        self.assertTrue(isinstance(model.people, People))

        # the values was passed through of {model_name}_kwargs are assigned
        # to the model instance
        self.assertEqual(model.people.first_name, 'Freyja')

    """
    🔽🔽🔽 Generate one list of three peoples
    """
    def test_generate_models__list_of_three_peoples():
        # get credentials to the requests through of self.client.{method_name}
        # and generate one user
        models = [self.generate_models(people=True) for _ in range(0, 3)]

        # the result of previous generator is one list of three dictionary of
        # models
        self.assertEqual(len(models), 3)

        for model in models:
            # each element of list contains one dictionary of models
            self.assertEqual(len(model), 1)

            # each element of list contains one instance of people
            self.assertTrue('people' in model)

    """
    🔽🔽🔽 Generate one list of three peoples with the same city
    """
    def test_generate_models__list_of_three_peoples__with_the_same_city():
        # we can create one dict of models that are require for various models
        city_kwargs = {'name': 'Fólkvangr'}
        base = self.generate_models(city=True, city_kwargs=city_kwargs)

        # we can pass in it case the model city that is stored in base var, and
        # through of models named keywork we can pass the previous models, it
        # should be util to resolve cases of relationships
        models = [self.generate_models(people=True, models=base) for _ in range(0, 3)]

        # the result of previous generator is one list of three dictionary of
        # models
        self.assertEqual(len(models), 3)

        for model in models:
            # each element of list contains two dictionary of models
            self.assertEqual(len(model), 2)

            # each element of list contains one instance of people
            self.assertTrue('people' in model)

            # each element of list contains one instance of people
            self.assertTrue('city' in model)

            # each element of list contains the same city
            self.assertTrue(model.city.id, 1)
            self.assertTrue(model.city.name, 'Fólkvangr')

    """
    🔽🔽🔽 Generate one list of three peoples with the same city with the inject model style
    """
    def test_generate_models__list_of_three_peoples__with_the_same_city__with_inject_model_style():
        # we can create one dict of models that are require for various models
        city_kwargs = {'name': 'Fólkvangr'}
        base = self.generate_models(city=True, city_kwargs=city_kwargs)

        # we can pass in it case the model city that is stored in base var, and
        # through of models named keywork we can pass the previous models, it
        # should be util to resolve cases of relationships

        # we can pass one model, in it case the model city stored in base vars,
        # just need add the {model}=base.{model} or {model}=base['{model}']
        models = [self.generate_models(people=True, city=base.city) for _ in range(0, 3)]

        # the result of previous generator is one list of three dictionary of
        # models
        self.assertEqual(len(models), 3)

        for model in models:
            # each element of list contains two dictionary of models
            self.assertEqual(len(model), 2)

            # each element of list contains one instance of people
            self.assertTrue('people' in model)

            # each element of list contains one instance of people
            self.assertTrue('city' in model)

            # each element of list contains the same city
            self.assertTrue(model.city.id, 1)
            self.assertTrue(model.city.name, 'Fólkvangr')
```
