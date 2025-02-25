import pytest
from tests.bdd_helper import *
from common.postgres import *
from common.model import QuestionAnswer
from datetime import datetime


# Require postgress server

@pytest.mark.asyncio
async def test_question():
    Given("default db connection and qa")
    current = str(datetime.now())
    qa = QuestionAnswer(question="time", answer=current,time=current)

    When("create table")
    create_table("test")

    And("insert data, retrieve data")
    await insert_data(qa, table_name="test")

    r = await get_latest(limit=1, table_name="test")

    Then("it is expected")
    assert r[0].answer == current
