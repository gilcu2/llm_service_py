# import random
#
# import pytest
#
# from common.bdd_helper import Given, When, Then
# from common.kafka import *
#
#
# @pytest.mark.skip(reason="no way of currently testing this")
# def test_send_get():
#     Given("qa")
#     qa = QuestionAnswer(
#         question=f"How are you {random.randint(1, 1000)}?",
#         answer="I am fine",
#     )
#
#     When("send")
#     send_to_kafka(qa)
#
#     And("receive")
#     r = get_from_kafka(limit=1, group="testing")
#
#     Then("must be the expected")
#     assert len(r) >= 1
