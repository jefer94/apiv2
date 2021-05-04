# TokenMixin

Provide one helper to assert tokens

```py
# tests/urls/tests_endpoint.py
from rest_framework.test import APITestCase
from breathecode.tests.mixins import TokenMixin


class TestSuite(APITestCase, TokenMixin):
    """
    🔽🔽🔽 Assert if one string is one Sha256 hash
    """
    def test_assertToken():
        # we can pass one string to assert if it's one token
        self.assertToken('...{Hash}...')
```
