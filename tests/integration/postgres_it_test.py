from datetime import datetime

import pytest

from common.bdd_helper import And, Given, Then, When
from common.model import QuestionAnswer
from common.postgres import create_table, get_latest, insert_data


# Require postgress server


@pytest.mark.xdist_group(name="postgres")
@pytest.mark.asyncio
async def test_question():
    Given("default db connection and qa")
    current = str(datetime.now())
    qa = QuestionAnswer(question="time", answer=current, time=current)

    When("create table")
    create_table("test")

    And("insert data, retrieve data")
    await insert_data(qa, table_name="test")

    r = await get_latest(limit=1, table_name="test")

    Then("it is expected")
    assert r[0].answer == current
