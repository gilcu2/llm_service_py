from tests.bdd_helper import *
from common.model import Question
import os
import pytest
import httpx

API_ENDPOINT = os.getenv("API_ENDPOINT", "localhost:8080")


@pytest.mark.asyncio
async def test_question():
    Given("question")
    question = Question(question="What is France capital?")

    When("call endpoint")
    async with httpx.AsyncClient() as client:
        response_question = await client.post(f'http://{API_ENDPOINT}/question', json=dict(question))
        response_history = await client.get(f'http://{API_ENDPOINT}/history/?limit=1')

    Then("response is expected")
    assert response_question.status_code == 200
    assert "Paris" in response_question.json()["answer"]
    assert "Paris" in response_history.json()[0]["answer"]
