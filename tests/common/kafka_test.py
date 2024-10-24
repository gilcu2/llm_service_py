from tests.bdd_helper import *
from common.kafka import *
import random


def test_send_get():
    Given("qa")
    qa = QuestionAnswer(
        question=f"How are you {random.randint(1, 1000)}?",
        answer="I am fine",
    )

    When("send")
    send_to_kafka(qa)

    And("receive")
    r = get_from_kafka(limit=1,group="testing")

    Then("must be the expected")
    assert len(r) >= 1

