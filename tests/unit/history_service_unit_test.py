from history_service.history_service import app
from tests.bdd_helper import *
from fastapi.testclient import TestClient
from pytest_httpx import HTTPXMock
from pytest_mock import MockFixture

client = TestClient(app)

def test_history_post(mocker: MockFixture , httpx_mock: HTTPXMock):
    Given("question and mocking external calls")
    question = "How are you doing"
    mocked_response={"question": "Hello", "answer": "Hi"}
    httpx_mock.add_response(json=mocked_response)
    mocker.patch("api_service.api_service.insert_data")


    When("call endpoint")
    response = client.post("/question", content=question.encode())

    Then("response is expected")
    assert response.status_code == 200
    assert response.json() == mocked_response

def test_history_get():
    Given("limit")
    limit = 1

    When("call endpoint")
    response = client.get("/history/?limit=1")

    Then("response is expected")
    assert response.status_code == 200
    response_list = response.json()
    assert len(response_list) == 1
    assert len(response_list[0]["answer"]) > 0
