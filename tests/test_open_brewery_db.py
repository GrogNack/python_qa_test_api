import pytest
import requests
import cerberus
import json


class TestOpenBreweryDB:
    base_url = "https://api.openbrewerydb.org/breweries"

    with open("../data/schema.json", "r") as f:
        schema = json.loads(f.read())

    @pytest.mark.parametrize("count", [i for i in range(25, 38, 3)])
    @pytest.mark.parametrize("city", ["san_francisco", "san_diego"])
    def test_brewery_by_city(self, count, city):
        parameters = {"by_city": city, "per_page": count}
        result = requests.get(self.base_url, params=parameters)
        assert result.status_code == 200
        result = result.json()
        v = cerberus.Validator()
        for res in result:
            assert v.validate(res, self.schema)
        assert len(result) == count

    @pytest.mark.parametrize("id", [i for i in range(2344, 2348, 2)])
    def test_get_single_brewery(self, id):
        response = requests.get(self.base_url + f"/{id}")
        v = cerberus.Validator()
        assert response.status_code == 200
        assert v.validate(response.json(), self.schema)

    def test_brewery_by_state(self):
        parameters = {"by_state": "ohio"}
        result = requests.get(self.base_url, params=parameters)
        assert result.status_code == 200
        result = result.json()
        v = cerberus.Validator()
        for res in result:
            assert v.validate(res, self.schema)
        assert len(result) == 20

    def test_brewery_by_type(self):
        parameters = {"by_type": "micro", "per_page": 30}
        result = requests.get(self.base_url, params=parameters)
        assert result.status_code == 200
        result = result.json()
        v = cerberus.Validator()
        for res in result:
            assert v.validate(res, self.schema)
            assert res["brewery_type"] == "micro"
        assert len(result) == 30

    @pytest.mark.parametrize("value", ["dog", "beer"])
    def test_autocomplete(self, value):
        response = requests.get(self.base_url + "/autocomplete" + f'?query={value}')
        schema = {
            "id": {"type": "string"},
            "name": {"type": "string"}
        }
        assert response.status_code == 200
        response = response.json()
        v = cerberus.Validator()
        for res in response:
            assert v.validate(res, schema)
            flag = res["name"].lower().find(value) + 1  # find substring in name of brewery
            assert flag
