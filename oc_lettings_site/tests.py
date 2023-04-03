from django.urls import reverse


def test_index(client):
    response = client.get(reverse('index'))
    assert "Welcome to Holiday Homes" in response.content
    assert response.status_code == 200
