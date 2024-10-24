import logging
import sys
import os
import psycopg2
from datetime import datetime
from common.model import QuestionAnswer

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(sys.stdout)
log_formatter = logging.Formatter(
    "%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s")
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)

POSTGRES_ENDPOINT = os.getenv("POSTGRES_ENDPOINT", "localhost:5432")
logger.debug(f"postgresendpoint: {POSTGRES_ENDPOINT}")

(host, port) = POSTGRES_ENDPOINT.split(":")
conn = psycopg2.connect(database="postgres",
                        user='user', password='pwd',
                        host=host, port=port
                        )
cursor = conn.cursor()


def create_table(table_name: str = "history"):
    sql = f'''
    CREATE TABLE IF NOT EXISTS {table_name} (
        event_id BIGSERIAL PRIMARY KEY, 
        event_time BIGINT NOT NULL, 
        question text, 
        answer text 
    );

    CREATE INDEX IF NOT EXISTS {table_name}_event_time ON {table_name} (
        event_time DESC
    );    
    '''
    cursor.execute(sql)
    conn.commit()


def insert_data(qa:QuestionAnswer, table_name: str = "history"):
    fields = ["event_time", "question", "answer"]
    fields_str = ',\n'.join(fields)
    sql = f"""
        INSERT INTO {table_name} (
            {fields_str}
        ) 
        VALUES(%s,%s,%s);
    """
    values=[datetime.now().timestamp(), qa.question, qa.answer]
    cursor.execute(sql, values)
    conn.commit()

def get_latest(limit:int=10, table_name: str = "history" ) -> list[QuestionAnswer]:
    fields = ["question", "answer"]
    fields_str = ',\n'.join(fields)
    sql = f"""        
        SELECT 
	        {fields_str}   
        FROM {table_name}
        ORDER BY event_id desc
        LIMIT {limit};
    """

    cursor.execute(sql)
    records = cursor.fetchall()
    output = []
    for row in records:
        output.append(QuestionAnswer(question=row[0], answer=row[1]))
    return output