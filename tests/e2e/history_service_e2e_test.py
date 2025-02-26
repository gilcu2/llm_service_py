import os
from datetime import datetime

import httpx
import pytest

from common.bdd_helper import Given, Then, When
from common.model import QuestionAnswer

current = str(datetime.now())

HISTORY_ENDPOINT = os.getenv("HISTORY_ENDPOINT", "localhost:8083")


@pytest.mark.xdist_group(name="postgres")
@pytest.mark.asyncio
async def test_history():
    Given("question_answer")
    question_answer = QuestionAnswer(question="Hello", answer="Hi", time=current)

    When("call endpoint")
    async with httpx.AsyncClient() as client:
        await client.post(
            f"http://{HISTORY_ENDPOINT}/history", json=dict(question_answer)
        )
        response = await client.get(f"http://{HISTORY_ENDPOINT}/history/?limit=1")

    Then("response is expected")
    assert response.status_code == 200
    response_list = response.json()
    assert len(response_list) == 1
    # assert response_list[0]["answer"] == question_answer.answer
