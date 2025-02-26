import random
from datetime import datetime

import pytest

from common.bdd_helper import And, Given, Then, When
from common.kafka_async import get_from_kafka, send_to_kafka
from common.model import QuestionAnswer

time_str = str(datetime.now())


@pytest.mark.asyncio
async def test_send_get():
    Given("qa")
    qa = QuestionAnswer(
        question=f"How are you {random.randint(1, 1000)}?",
        answer="I am fine",
        time=time_str,
    )

    When("send")
    await send_to_kafka(qa)

    And("receive")
    r = await get_from_kafka(limit=1)

    Then("must be the expected")
    assert len(r) >= 1
    assert r[-1] == qa
