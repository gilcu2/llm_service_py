from tests.bdd_helper import *
from common.model import QuestionAnswer
from common.postgres import *

def test_history_table():
    Given("table some data")
    qa1=QuestionAnswer(question="q1",answer="answer1")
    qa2 = QuestionAnswer(question="q2", answer="answer2")

    When("create table, insert and retrieve data")
    create_table()
    insert_data(qa1)
    insert_data(qa2)
    r=get_latest(limit=2)


    Then("it is ok")
    assert r == [qa2,qa1]