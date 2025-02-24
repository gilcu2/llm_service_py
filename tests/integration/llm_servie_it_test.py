from llm_service.llm_service import app
from tests.bdd_helper import *
from fastapi.testclient import TestClient
from common.model import Question, QuestionAnswer


client = TestClient(app)

def test_question():
    Given("question and mocking httpx")
    question = Question(question="What is France capital?")

    When("call endpoint")
    response = client.post("/question", json=dict(question))

    Then("response is expected")
    assert response.status_code == 200
    assert "Paris" in response.json()["answer"]