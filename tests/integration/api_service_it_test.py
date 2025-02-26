from api_service.api_service import app
from tests.bdd_helper import *
from fastapi.testclient import TestClient
from common.model import Question, QuestionAnswer


client = TestClient(app)

def test_question():
    Given("question")
    question = Question(question="What is France capital?")

    When("call endpoint")
    response = client.post("/question", json=dict(question))

    Then("response is expected")
    assert response.status_code == 200
    assert "Paris" in response.json()["answer"]

def test_history():
    Given("limit")
    limit=2

    When("call endpoint")
    response = client.get(f"/history/?limit={limit}")

    Then("response is expected")
    assert response.status_code == 200
    r=response.json()
    assert len(r) > 1