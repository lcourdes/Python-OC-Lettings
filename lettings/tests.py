import pytest
from django.urls import reverse


@pytest.fixture(scope='session')
def django_db_setup():
    django_db_use_migrations = False
    return django_db_use_migrations


@pytest.mark.django_db()
def test_lettings_index(client):
    response = client.get(reverse('lettings:index'))
    assert "<title>Lettings</title>" in response.content.decode()
    assert response.status_code == 200


@pytest.mark.django_db()
def test_lettings(client):
    response = client.get(reverse('lettings:letting', args=["1"]))
    assert "<h1>Joshua Tree Green Haus /w Hot Tub</h1>" in response.content.decode()
    assert response.status_code == 200
