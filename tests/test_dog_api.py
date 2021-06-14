import json
from unittest.mock import patch

import cerberus
import pytest
import requests

from mocks.mock_dog_api import mock_request_all_bread, mock_request_images_bread, mock_request_random_image


class TestDogAPI:
    base_url = "https://dog.ceo/api"

    @patch('requests.get',
           return_value='{"message":"https:\/\/images.dog.ceo\/breeds\/sheepdog-shetland\/n02105855_19782.jpg","status":"success"}')
    def test_single_random_image_methods(self, mock_requests):
        schema = {
            "message": {"type": "string"},
            "status": {"type": "string"}
        }
        result = requests.get(self.base_url + '/breeds/image/random2')
        v = cerberus.Validator()
        # assert result.status_code == 200
        assert v.validate(json.loads(result), schema)

    @patch.object(requests, 'get', return_value=mock_request_all_bread())
    def test_list_all_breeds(self, mock_requests):
        schema = {
            "message": {"type": "dict"},
            "status": {"type": "string"}
        }
        result = requests.get(self.base_url + '/breeds/list/all')
        v = cerberus.Validator()
        assert result.status_code == 200
        assert v.validate(result.json(), schema)

    @patch.object(requests, 'get', return_value=mock_request_images_bread())
    @pytest.mark.parametrize("breed", ["chow", "chihuahua", "briard", "boxer"])
    def test_list_images_by_breed(self, mock_requests, breed):
        schema = {
            "message": {"type": "list"},
            "status": {"type": "string"}
        }
        result = requests.get(self.base_url + f'/breed/{breed}/images')
        v = cerberus.Validator()
        assert result.status_code == 200
        assert v.validate(result.json(), schema)

    @patch('requests.get', return_value=mock_request_random_image())
    @pytest.mark.parametrize("breed", ["basenji", "borzoi", "buhund", "cattledog"])
    def test_random_image_by_breed(self, mock_requests, breed):
        schema = {
            "message": {"type": "string"},
            "status": {"type": "string"}
        }
        result = requests.get(self.base_url + f'/breed/{breed}/images/random')
        v = cerberus.Validator()
        assert result.status_code == 200
        assert v.validate(result.json(), schema)
