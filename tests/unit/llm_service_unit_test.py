from datetime import datetime

from fastapi.testclient import TestClient
from pytest_mock import MockFixture

from common.bdd_helper import And, Given, Then, When
from common.model import Question, QuestionAnswer
from llm_service.llm_service import app

current = str(datetime.now())

client = TestClient(app)


def test_question(mocker: MockFixture):
    Given("question and mocking httpx")
    question = Question(question="Hello")
    mocked_response = QuestionAnswer(question="Hello", answer="Hi", time=current)

    And("Mocking external calls")
    mocker.patch(
        "llm_service.llm_service.ask_ollama", return_value=mocked_response.answer
    )

    When("call endpoint")
    response = client.post("/question", json=dict(question))

    Then("response is expected")
    assert response.status_code == 200
    assert response.json()["answer"] == mocked_response.answer
