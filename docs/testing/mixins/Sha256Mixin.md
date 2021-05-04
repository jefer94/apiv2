# Sha256Mixin

Provide one helper check sha256 hashs

```py
# tests/urls/tests_endpoint.py
from rest_framework.test import APITestCase
from breathecode.tests.mixins import Sha256Mixin


class TestSuite(APITestCase, Sha256Mixin):
    """
    🔽🔽🔽 Assert if one string is one Sha256 hash
    """
    def test_assertHash():
        # we can pass one string to assert if it's one sha256 hash
        self.assertHash('...{Hash}...')
```
