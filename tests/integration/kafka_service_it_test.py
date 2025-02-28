import random
from datetime import datetime

import pytest

from common.bdd_helper import And, Given, Then, When
from common.kafka_async import get_from_kafka, send_to_kafka
from kafka_service.kafka_service import update_postgres
from common.postgres import get_latest
from common.model import QuestionAnswer
import asyncio

time_str = str(datetime.now())


@pytest.mark.asyncio
async def test_update_postgres():
    Given("update postgres running in backgroud")
    asyncio.create_task(update_postgres())

    qa = QuestionAnswer(
        question=f"How are you {random.randint(1, 1000)}?",
        answer="I am fine",
        time=time_str,
    )

    When("send to kafka")
    await send_to_kafka(qa)

    And("receive from postgres")
    await asyncio.sleep(1)
    r = await get_latest(limit=1)

    Then("must be the expected")
    assert len(r) >= 1
    assert r[-1] == qa


