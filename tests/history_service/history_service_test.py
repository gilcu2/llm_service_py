from history_service.history_service import app
from tests.bdd_helper import *
from fastapi.testclient import TestClient

client = TestClient(app)


def test_history():
    Given("limit")
    limit = 1

    When("call endpoint")
    response = client.get("/history/?limit=1")

    Then("response is expected")
    assert response.status_code == 200
    response_list = response.json()
    assert len(response_list) == 1
    assert len(response_list[0]["answer"]) > 0
