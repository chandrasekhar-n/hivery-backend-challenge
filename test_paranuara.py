import pytest
import json

from paranuara.app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    yield client


def test_get_person_invalid(client):
    response = client.get("/api/v1/getPeople/abcd")
    assert response.status_code == 404
    assert response.json == {
                            'message': 'Unable to fetch query parameter, Provide valid person name, email, id or index'
                            }


def test_get_person_byindex_none(client):
    response = client.get("/api/v1/getPeople")
    assert response.status_code == 404



def test_get_person_byindex(client):
    response = client.get("/api/v1/getPeople/0")

    assert response.status_code == 200


def test_get_person_byname(client):
    response = client.get("/api/v1/getPeople/CarmellaLambert")

    assert response.status_code == 200


def test_get_person_byid(client):
    response = client.get("/api/v1/getPeople/595eeb9b96d80a5bc7afb106")

    assert response.status_code == 200


def test_get_person_byid(client):
    response = client.get("/api/v1/getPeople/595eeb9b96d80a5bc7afb106")

    assert response.status_code == 200


def test_get_person_byid(client):
    response = client.get("/api/v1/getPeople/595eeb9b96d80a5bc7afb106")

    assert response.status_code == 200


def test_get_multipeople_invlaid(client):
    headers = {'Content-Type': 'application/json'}
    response = client.post('/api/v1/getMultiPeople',data = json.dumps(["test1","test2"]),headers = headers)
    assert response.status_code == 404
    assert response.json == {
                                "message": "Unable to fetch People [u'test1', u'test2'], Provide valid name or index"
                            }

def test_get_multipeople_validindex(client):
    headers = {'Content-Type': 'application/json'}
    response = client.post('/api/v1/getMultiPeople',data = json.dumps(["0","1"]),headers = headers)
    assert response.status_code == 200


def test_get_companyemployees_invalid(client):
    response = client.get("/api/v1/getCompanyEmployees/abcd")
    assert response.status_code == 404
    assert response.json == {
                            'message': 'Unable to fetch company, Provide valid company name or index'
                            }

def test_get_companyemployees_valid(client):
    response = client.get("/api/v1/getCompanyEmployees/0")
    assert response.status_code == 200
    assert len(response.json) > 0
