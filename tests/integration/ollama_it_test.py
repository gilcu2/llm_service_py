import pytest

from common.bdd_helper import Given, Then, When
from common.ollama import ask_ollama

# Require postgress server


@pytest.mark.asyncio
async def test_ask_ollama():
    Given("question")
    question = "What is France capital?"

    When("call ollama")
    r = await ask_ollama(question)

    Then("it is expected")
    assert "Paris" in r
