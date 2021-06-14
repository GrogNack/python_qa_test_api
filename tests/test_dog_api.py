import json
from unittest.mock import Mock
from unittest.mock import patch

import cerberus
import pytest
import requests


def mock_request_all_bread():
    response_mock = Mock()
    response_mock.status_code = 200
    response_mock.json.return_value = {
        "message": {"affenpinscher": [], "african": [], "airedale": [], "akita": [], "appenzeller": [],
                    "australian": ["shepherd"], "basenji": [], "beagle": [], "bluetick": [], "borzoi": [],
                    "bouvier": [], "boxer": [], "brabancon": [], "briard": [], "buhund": ["norwegian"],
                    "bulldog": ["boston", "english", "french"], "bullterrier": ["staffordshire"], "cairn": [],
                    "cattledog": ["australian"], "chihuahua": [], "chow": [], "clumber": [], "cockapoo": [],
                    "collie": ["border"], "coonhound": [], "corgi": ["cardigan"], "cotondetulear": [], "dachshund": [],
                    "dalmatian": [], "dane": ["great"], "deerhound": ["scottish"], "dhole": [], "dingo": [],
                    "doberman": [], "elkhound": ["norwegian"], "entlebucher": [], "eskimo": [],
                    "finnish": ["lapphund"], "frise": ["bichon"], "germanshepherd": [], "greyhound": ["italian"],
                    "groenendael": [], "havanese": [],
                    "hound": ["afghan", "basset", "blood", "english", "ibizan", "plott", "walker"], "husky": [],
                    "keeshond": [], "kelpie": [], "komondor": [], "kuvasz": [], "labradoodle": [], "labrador": [],
                    "leonberg": [], "lhasa": [], "malamute": [], "malinois": [], "maltese": [],
                    "mastiff": ["bull", "english", "tibetan"], "mexicanhairless": [], "mix": [],
                    "mountain": ["bernese", "swiss"], "newfoundland": [], "otterhound": [], "ovcharka": ["caucasian"],
                    "papillon": [], "pekinese": [], "pembroke": [], "pinscher": ["miniature"], "pitbull": [],
                    "pointer": ["german", "germanlonghair"], "pomeranian": [],
                    "poodle": ["miniature", "standard", "toy"], "pug": [], "puggle": [], "pyrenees": [], "redbone": [],
                    "retriever": ["chesapeake", "curly", "flatcoated", "golden"], "ridgeback": ["rhodesian"],
                    "rottweiler": [], "saluki": [], "samoyed": [], "schipperke": [],
                    "schnauzer": ["giant", "miniature"], "setter": ["english", "gordon", "irish"],
                    "sheepdog": ["english", "shetland"], "shiba": [], "shihtzu": [],
                    "spaniel": ["blenheim", "brittany", "cocker", "irish", "japanese", "sussex", "welsh"],
                    "springer": ["english"], "stbernard": [],
                    "terrier": ["american", "australian", "bedlington", "border", "dandie", "fox", "irish",
                                "kerryblue", "lakeland", "norfolk", "norwich", "patterdale", "russell", "scottish",
                                "sealyham", "silky", "tibetan", "toy", "westhighland", "wheaten", "yorkshire"],
                    "vizsla": [], "waterdog": ["spanish"], "weimaraner": [], "whippet": [], "wolfhound": ["irish"]},
        "status": "success"
    }
    return response_mock


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
