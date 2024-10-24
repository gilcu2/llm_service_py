from api_service.api_service import app
from tests.bdd_helper import *
from fastapi.testclient import TestClient


client = TestClient(app)


def test_question():
    Given("question")
    question = "How are you doing"

    When("call endpoint")
    response = client.post("/question_llama", content=question.encode())

    Then("response is expected")
    assert response.status_code == 200
    assert response.json() == {
        "question": question,
        "answer": "Hi"
    }
