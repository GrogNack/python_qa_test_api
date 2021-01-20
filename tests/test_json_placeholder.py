import json

import cerberus
import pytest
import requests


class TestJsonPlaceHolder:
    base_url = "https://jsonplaceholder.typicode.com"

    with open("../data/schema_user.json", "r") as f:
        schema = json.loads(f.read())

    def test_users(self):
        v = cerberus.Validator()
        respons = requests.get(self.base_url + "/users")
        assert respons.status_code == 200
        respons = respons.json()
        assert len(respons) == 10
        for res in respons:
            assert v.validate(res, self.schema)

    @pytest.mark.parametrize("id", [1, 2, 3, 4])
    def test_comments(self, id):
        schema = {
            "postId": {"type": "integer"},
            "id": {"type": "integer"},
            "name": {"type": "string"},
            "email": {"type": "string"},
            "body": {"type": "string"}
        }
        v = cerberus.Validator()
        respons = requests.get(self.base_url + f"/comments?postId={id}")
        assert respons.status_code == 200
        respons = respons.json()
        assert len(respons) == 5
        for res in respons:
            assert res["postId"] == id
            assert v.validate(res, schema)

    @pytest.mark.parametrize("id", ["a", -2, "%"], ids=["Char", "Negative number", "Spec"])
    def test_comments_negative(self, id):
        respons = requests.get(self.base_url + f"/comments?postId={id}")
        assert respons.status_code == 200
        respons = respons.json()
        assert len(respons) == 0
        assert respons == []

    @pytest.mark.parametrize("title, body, userId",
                             [("title1", "body1", 1), ("title2", "body2", 2), ("title3", "body3", 3)])
    def test_create_post(self, title, body, userId):
        data = {
            "title": title,
            "body": body,
            "userId": userId
        }
        respons = requests.post(self.base_url + "/posts", data=data)
        assert respons.status_code == 201
        respons = respons.json()
        assert respons["title"] == title
        assert respons["body"] == body
        assert respons["userId"] == str(userId)

    def test_delete(self):
        respons = requests.delete(self.base_url + "/posts/1")
        assert respons.status_code == 200
        respons = respons.json()
        assert len(respons) == 0
