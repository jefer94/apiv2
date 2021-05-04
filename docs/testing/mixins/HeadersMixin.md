# HeadersMixin

Provide one helper to handle headers

```py
# tests/urls/tests_endpoint.py
from rest_framework.test import APITestCase
from breathecode.tests.mixins import HeadersMixin


class TestSuite(APITestCase, HeadersMixin):
    """
    🔽🔽🔽 Add some headers to self.client
    """
    def test_headers():
        # add N headers to the self.client
        self.headers(academy=1, cache_control='no-cache')

        # this request include the Academy and Cache-Control headers
        self.client.get('https://www.youtube.com')
```
