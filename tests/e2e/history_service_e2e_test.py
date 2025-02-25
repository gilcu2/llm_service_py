from tests.bdd_helper import *
from common.model import QuestionAnswer
import os
import pytest
import httpx
from datetime import datetime

current = str(datetime.now())

HISTORY_ENDPOINT = os.getenv("HISTORY_ENDPOINT", "localhost:8083")


@pytest.mark.asyncio
async def test_history():
    Given("question_answer and mocking external calls")
    question_answer = QuestionAnswer(question="Hello", answer="Hi", time=current)

    When("call endpoint")
    async with httpx.AsyncClient() as client:
        await client.post(f'http://{HISTORY_ENDPOINT}/history', json=dict(question_answer))
        response = await client.get(f'http://{HISTORY_ENDPOINT}/history/?limit=1')

    Then("response is expected")
    assert response.status_code == 200
    response_list = response.json()
    assert len(response_list) == 1
    assert response_list[0]["answer"] == question_answer.answer
