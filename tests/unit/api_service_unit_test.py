from api_service.api_service import app, ask_question, to_history
from tests.bdd_helper import *
from fastapi.testclient import TestClient
from pytest_httpx import HTTPXMock
from pytest_mock import MockFixture
from common.model import Question, QuestionAnswer
import pytest
from datetime import datetime

current = str(datetime.now())


@pytest.mark.asyncio
async def test_ask_question(httpx_mock: HTTPXMock):
    Given("question and mocking external calls")
    question = Question(question="How are you doing")
    mocked_response = {"question": "Hello", "answer": "Hi", "time": current}
    httpx_mock.add_response(json=mocked_response)

    When("call")
    r = await ask_question(question)

    Then("response is expected")
    assert r == QuestionAnswer.model_validate(mocked_response)


@pytest.mark.asyncio
async def test_to_history(httpx_mock: HTTPXMock):
    Given("question_answer and mocking external calls")
    question_answer = QuestionAnswer(question="How are you doing", answer="hi", time=current)
    mocked_response = ""
    httpx_mock.add_response(text=mocked_response)

    When("call")
    r = await to_history(question_answer)

    Then("response is expected")
    assert r


@pytest.mark.asyncio
async def test_get_histories(httpx_mock: HTTPXMock):
    Given("question_answer and mocking external calls")
    question_answer = QuestionAnswer(question="How are you doing", answer="hi", time=current)
    httpx_mock.add_response(json=[dict(question_answer)])

    When("call")
    r = await to_history(question_answer)

    Then("response is expected")
    assert r


def test_question(mocker: MockFixture):
    Given("question and answer")
    question = Question(question="How are you doing")
    mocked_response = QuestionAnswer(question="Hello", answer="Hi", time=current)

    And("Mocking external calls")
    mocker.patch("api_service.api_service.ask_question", return_value=mocked_response)
    mocker.patch("api_service.api_service.to_history", return_value=True)

    client = TestClient(app)

    When("call endpoint")
    response = client.post("/question", json=dict(question))

    Then("response is expected")
    assert response.status_code == 200
    assert response.json() == dict(mocked_response)


def test_history(mocker: MockFixture):
    Given("question and answer")
    mocked_response = QuestionAnswer(question="Hello", answer="Hi", time=current)

    And("Mocking external calls")
    mocker.patch("api_service.api_service.get_histories", return_value=[mocked_response])

    client = TestClient(app)

    When("call endpoint")
    response = client.get("/history")

    Then("response is expected")
    assert response.status_code == 200
    assert response.json() == [dict(mocked_response)]
