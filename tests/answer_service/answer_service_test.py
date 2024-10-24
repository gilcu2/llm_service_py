from answer_service.answer_service import app
from tests.bdd_helper import *
from fastapi.testclient import TestClient
import random

client = TestClient(app)


def test_question_and_queue():
    Given("question")
    question = f"How are you doing {random.randint(1, 1000)}"

    When("call endpoint")
    response = client.post("/question", content=question.encode())

    Then("response is expected")
    assert response.status_code == 200
    response_dict=response.json()
    assert response_dict["question"] == question
    assert len(response_dict["answer"]) > 0

    


