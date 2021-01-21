import cerberus
import pytest
import requests


class TestDogAPI:
    base_url = "https://dog.ceo/api"

    def test_single_random_image_methods(self):
        schema = {
            "message": {"type": "string"},
            "status": {"type": "string"}
        }
        result = requests.get(self.base_url + '/breeds/image/random')
        v = cerberus.Validator()
        assert result.status_code == 200
        assert v.validate(result.json(), schema)

    def test_list_all_breeds(self):
        schema = {
            "message": {"type": "dict"},
            "status": {"type": "string"}
        }
        result = requests.get(self.base_url + '/breeds/list/all')
        v = cerberus.Validator()
        assert result.status_code == 200
        assert v.validate(result.json(), schema)

    @pytest.mark.parametrize("breed", ["chow", "chihuahua", "briard", "boxer"])
    def test_list_images_by_breed(self, breed):
        schema = {
            "message": {"type": "list"},
            "status": {"type": "string"}
        }
        result = requests.get(self.base_url + f'/breed/{breed}/images')
        v = cerberus.Validator()
        assert result.status_code == 200
        assert v.validate(result.json(), schema)

    @pytest.mark.parametrize("breed", ["basenji", "borzoi", "buhund", "cattledog"])
    def test_random_image_by_breed(self, breed):
        schema = {
            "message": {"type": "string"},
            "status": {"type": "string"}
        }
        result = requests.get(self.base_url + f'/breed/{breed}/images/random')
        v = cerberus.Validator()
        assert result.status_code == 200
        assert v.validate(result.json(), schema)

    @pytest.mark.parametrize("breed", ["basenji", "borzoi", "buhund", "cattledog"])
    def test_all_sub_breed(self, breed):
        schema = {
            "message": {"type": "list"},
            "status": {"type": "string"}
        }
        result = requests.get(self.base_url + f'/breed/{breed}/list')
        v = cerberus.Validator()
        assert result.status_code == 200
        assert v.validate(result.json(), schema)
