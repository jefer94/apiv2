"""
Test /answer
"""

import capyc.pytest as capy
import pytest
from django.urls.base import reverse_lazy
from django.utils import timezone
from rest_framework import status

UTC_NOW = timezone.now()


@pytest.fixture(autouse=True)
def setup(db):
    yield


@pytest.mark.parametrize(
    "op_type, expected",
    [
        ("media", {"chunk_size": 10485760, "max_chunks": None}),
        ("proof-of-payment", {"chunk_size": 10485760, "max_chunks": None}),
        ("profile-picture", {"chunk_size": 10485760, "max_chunks": 25}),
    ],
)
def test_op_type_desc(client: capy.Client, op_type: str, expected: dict):
    url = reverse_lazy("v2:media:operationtype_type", kwargs={"op_type": op_type})

    response = client.get(url)

    json = response.json()

    assert json == expected
    assert response.status_code == status.HTTP_200_OK
