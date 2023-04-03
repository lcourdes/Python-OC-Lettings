import pytest
from django.urls import reverse


@pytest.fixture(scope='session')
def django_db_setup():
    django_db_use_migrations = False
    return django_db_use_migrations


@pytest.mark.django_db()
def test_profile_index(client):
    response = client.get(reverse('profiles:index'))
    assert "<title>Profiles</title>" in response.content.decode()
    assert response.status_code == 200


@pytest.mark.django_db()
def test_profile(client):
    response = client.get(reverse('profiles:profile', args=["HeadlinesGazer"]))
    assert "<h1>HeadlinesGazer</h1>" in response.content.decode()
    assert response.status_code == 200
