# DatetimeMixin

Provide one helper to handle datetime instances of datetime in iso format

```py
# tests/urls/tests_endpoint.py
from rest_framework.test import APITestCase
from datetime import datetime
from breathecode.tests.mixins import DatetimeMixin


class TestSuite(APITestCase, DatetimeMixin):
    """
    🔽🔽🔽 Get one instance of datetime with current date and time
    """
    def test_datetime_now():
        # return one datetime instance with current date and time
        self.assertTrue(isinstance(self.date_today(), datetime))

    """
    🔽🔽🔽 Get one datetime with current date and time in iso format
    """
    def test_datetime_to_iso():
        # return one datetime with current date and time in iso format
        self.assertEqual(self.datetime_to_iso(datetime.now()), '2021-05-04T01:18:16.068Z')

    """
    🔽🔽🔽 Get one datetime with current date and time in ical format
    """
    def test_datetime_to_ical():
        # return one datetime with current date and time in ical format
        self.assertEqual(self.datetime_to_ical(datetime.now()), '20210504T012423Z')

    """
    🔽🔽🔽 Get one datetime with current date and time in ical format
    """
    def test_assertDatetime():
        # check if the parameter is one datetime instance
        self.assertDatetime(datetime.now())

        # check if the parameter is one datetime is iso format
        self.assertDatetime('2021-05-04T01:18:16.068Z')
```
