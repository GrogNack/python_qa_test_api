## Homework "API Testing"

### Installation
This project use pipenv
```
pip install pipenv
pipenv shell
pipenv install
```
### Runnung
1. Test for DogAPI `pytest -v ./tests/test_dog_api.py`
2. Test for openbrewerydb `pytest -v ./tests/test_open_brewery_db.py`
3. Test for jsonplaceholder `pytest -v ./tests/test_json_placeholder.py`
4. Test status code for same url `pytest -v --url <URL> --status_code <expectet status code> ./tests/test_addoption.py`