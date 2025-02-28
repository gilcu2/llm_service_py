import logging
import sys

from fastapi import BackgroundTasks, FastAPI

from common.model import QuestionAnswer
from common.postgres import create_table, get_latest, insert_data

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(sys.stdout)
log_formatter = logging.Formatter(
    "%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] "
    "[%(levelname)s] %(name)s: %(message)s"
)
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)

app = FastAPI()


@app.get("/history/")
async def get_latest_histories(limit: int = 10):
    qas = await get_latest(limit)
    return qas


@app.post("/history")
async def add_history(qa: QuestionAnswer, background_tasks: BackgroundTasks):
    background_tasks.add_task(insert_data, qa)


if __name__ == "__main__":
    create_table()
