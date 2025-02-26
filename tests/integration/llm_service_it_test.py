from fastapi.testclient import TestClient

from common.bdd_helper import Given, Then, When
from common.model import Question
from llm_service.llm_service import app

client = TestClient(app)


def test_question():
    Given("question")
    question = Question(question="What is France capital?")

    When("call endpoint")
    response = client.post("/question", json=dict(question))

    Then("response is expected")
    assert response.status_code == 200
    assert "Paris" in response.json()["answer"]
