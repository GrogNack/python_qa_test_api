import requests


def test_pytest_addoption(base_url, request_status_code):
    response = requests.get(base_url)
    assert response.status_code == int(request_status_code)
