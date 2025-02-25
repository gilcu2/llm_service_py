from tests.bdd_helper import *
from common.model import Question
import os
import pytest
import httpx

LLM_ENDPOINT = os.getenv("LLM_ENDPOINT", "localhost:8082")


@pytest.mark.asyncio
async def test_question():
    Given("question")
    question = Question(question="What is France capital?")

    When("call endpoint")
    async with httpx.AsyncClient() as client:
        response = await client.post(f'http://{LLM_ENDPOINT}/question', json=dict(question))

    Then("response is expected")
    assert response.status_code == 200
    assert "Paris" in response.json()["answer"]
