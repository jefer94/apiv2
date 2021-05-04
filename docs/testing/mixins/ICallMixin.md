# ICallMixin

Provide one helper to handle ical files

```py
# tests/urls/tests_endpoint.py
from rest_framework.test import APITestCase
from datetime import datetime
from breathecode.tests.mixins import ICallMixin


class TestSuite(APITestCase, ICallMixin):
    """
    🔽🔽🔽 Add one limit to characters to line and add one linebreak
    """
    def test_line_limit():
        # one string with 90 characters
        line = 'SUMMARY: This is the ...{53 characters}... enjoy the event'

        expected = '\n'.join([
            'SUMMARY: This is the ...{53 characters}...',
            '  enjoy the event',
        ])

        # in each 74 char of line, if add one space and continue in the next line
        self.assertEqual(self.line_limit(line), expected)
```
