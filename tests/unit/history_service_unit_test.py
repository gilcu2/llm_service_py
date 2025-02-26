from datetime import datetime

from fastapi.testclient import TestClient
from pytest_mock import MockFixture

from common.bdd_helper import Given, Then, When
from common.model import QuestionAnswer
from history_service.history_service import app

current = str(datetime.now())

client = TestClient(app)


def test_add_history(mocker: MockFixture):
    Given("question_answer and mocking external calls")
    question_answer = QuestionAnswer(question="Hello", answer="Hi", time=current)
    mocker.patch("history_service.history_service.insert_data")


    When("call endpoint")
    response = client.post("/history", json=dict(question_answer))

    Then("response is expected")
    assert response.status_code == 200


def test_get_latest_histories(mocker: MockFixture):
    Given("mocked get_latest")
    question_answer = QuestionAnswer(question="Hello", answer="Hi", time=current)
    mocker.patch(
        "history_service.history_service.get_latest", return_value=[question_answer]
    )

    When("call endpoint")
    response = client.get("/history/?limit=1")

    Then("response is expected")
    assert response.status_code == 200
    response_list = response.json()
    assert len(response_list) == 1
    assert response_list[0] == dict(question_answer)
