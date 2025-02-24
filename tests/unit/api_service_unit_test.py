from api_service.api_service import app, ask_question, save_question_answer
from tests.bdd_helper import *
from fastapi.testclient import TestClient
from pytest_httpx import HTTPXMock
from pytest_mock import MockFixture
from common.model import Question, QuestionAnswer
import pytest


@pytest.mark.asyncio
async def test_ask_question(httpx_mock: HTTPXMock):
    Given("question and mocking external calls")
    question = Question(question="How are you doing")
    mocked_response = {"question": "Hello", "answer": "Hi"}
    httpx_mock.add_response(json=mocked_response)

    When("call")
    r = await ask_question(question)

    Then("response is expected")
    assert r == QuestionAnswer.model_validate(mocked_response)


@pytest.mark.asyncio
async def test_save_question_answer(httpx_mock: HTTPXMock):
    Given("question_answer and mocking external calls")
    question_answer = QuestionAnswer(question="How are you doing", answer="hi")
    mocked_response = ""
    httpx_mock.add_response(text=mocked_response)

    When("call")
    r = await save_question_answer(question_answer)

    Then("response is expected")
    assert r


def test_question(mocker: MockFixture):
    Given("question and answer")
    question = Question(question="How are you doing")
    mocked_response = QuestionAnswer(question="Hello", answer="Hi")

    And("Mocking external calls")
    mocker.patch("api_service.api_service.ask_question", return_value=mocked_response)
    mocker.patch("api_service.api_service.save_question_answer", return_value=True)

    client = TestClient(app)

    When("call endpoint")
    response = client.post("/question", json=dict(question))

    Then("response is expected")
    assert response.status_code == 200
    assert response.json() == dict(mocked_response)
