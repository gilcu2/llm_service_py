from api_service.api_service import app
from tests.bdd_helper import *
from fastapi.testclient import TestClient
from pytest_httpx import HTTPXMock


client = TestClient(app)

def test_question(httpx_mock: HTTPXMock):
    Given("question and mocking httpx")
    question = "How are you doing"
    mocked_response={"question": "Hello", "answer": "Hi"}
    httpx_mock.add_response(json=mocked_response)

    When("call endpoint")
    response = client.post("/question", content=question.encode())

    Then("response is expected")
    assert response.status_code == 200
    assert response.json() == mocked_response
