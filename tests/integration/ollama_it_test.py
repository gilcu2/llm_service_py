import pytest
from tests.bdd_helper import *
from common.ollama import *


# Require postgress server

@pytest.mark.asyncio
async def test_ask_ollama():
    Given("question")
    question = "What is France capital?"

    When("call ollama")
    r = await ask_ollama(question)

    Then("it is expected")
    assert "Paris" in r
