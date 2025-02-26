from datetime import datetime

from fastapi.testclient import TestClient

from common.bdd_helper import And, Given, Then, When
from common.model import QuestionAnswer
from history_service.history_service import app
import pytest

current = str(datetime.now())

client = TestClient(app)


@pytest.mark.xdist_group(name="postgres")
def test_add_get_history():
    Given("question_answer and mocking external calls")
    question_answer = QuestionAnswer(question="Hello", answer="Hi", time=current)

    When("add history")
    client.post("/history", json=dict(question_answer))

    And("get latest")
    response = client.get("/history/?limit=1")

    Then("response is expected")
    assert response.status_code == 200
    response_list = response.json()
    assert len(response_list) == 1
    assert response_list[0] == dict(question_answer)
