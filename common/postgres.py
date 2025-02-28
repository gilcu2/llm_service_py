import logging
import os
import sys
from datetime import datetime

import psycopg

from common.model import QuestionAnswer

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(sys.stdout)
log_formatter = logging.Formatter(
    "%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] "
    "[%(levelname)s] %(name)s: %(message)s"
)
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)

POSTGRES_ENDPOINT = os.getenv(
    "POSTGRES_ENDPOINT", "postgresql://user:pass@localhost:5432/postgres"
)
logger.debug(f"postgresendpoint: {POSTGRES_ENDPOINT}")


def create_table(table_name: str = "history"):
    sql = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        event_id BIGSERIAL PRIMARY KEY,
        event_time BIGINT NOT NULL,
        question text,
        answer text,
        time text
    );

    CREATE INDEX IF NOT EXISTS {table_name}_event_time ON {table_name} (
        event_time DESC
    );
    """
    with psycopg.connect(POSTGRES_ENDPOINT) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)


async def insert_data(qa: QuestionAnswer, table_name: str = "history"):
    fields = ["event_time", "question", "answer", "time"]
    fields_str = ",\n".join(fields)
    sql = f"""
        INSERT INTO {table_name} (
            {fields_str}
        )
        VALUES(%s,%s,%s,%s);
    """
    values = [datetime.now().timestamp(), qa.question, qa.answer, qa.time]

    async with await psycopg.AsyncConnection.connect(POSTGRES_ENDPOINT) as aconn:
        async with aconn.cursor() as acur:
            await acur.execute(sql, values)


async def get_latest(
    limit: int = 10, table_name: str = "history"
) -> list[QuestionAnswer]:
    fields = ["question", "answer", "time"]
    fields_str = ",\n".join(fields)
    sql = f"""
        SELECT
           {fields_str}
        FROM {table_name}
        ORDER BY event_id desc
        LIMIT {limit};
    """

    async with await psycopg.AsyncConnection.connect(POSTGRES_ENDPOINT) as aconn:
        async with aconn.cursor() as acur:
            await acur.execute(sql)
            r = await acur.fetchall()

            output = []
            for row in r:
                output.append(
                    QuestionAnswer(question=row[0], answer=row[1], time=row[2])
                )
            return output
