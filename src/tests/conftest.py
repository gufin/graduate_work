import pytest

from core.containers import Container


@pytest.fixture
def container():
    return Container()
