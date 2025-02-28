import asyncio
import logging
import os
import sys

from aiokafka import AIOKafkaConsumer  # type: ignore[import-untyped]

from common.model import QuestionAnswer
from common.postgres import insert_data

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(sys.stdout)
log_formatter = logging.Formatter(
    "%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] "
    "[%(levelname)s] %(name)s: %(message)s"
)
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)

KAFKA_ENDPOINT = os.getenv("KAFKA_ENDPOINT", "localhost:9092")
logger.debug(f"kafka enpoint: {KAFKA_ENDPOINT}")


async def update_postgres():
    consumer = AIOKafkaConsumer(
        "history",
        bootstrap_servers=KAFKA_ENDPOINT,
        auto_offset_reset="earliest",
        group_id="kafka_service_group",
    )
    await consumer.start()
    logger.debug("Consumer started")
    try:
        async for message in consumer:
            qa = QuestionAnswer.model_validate_json(message.value.decode())
            logger.debug("QA received from Kafka")
            await insert_data(qa)
            logger.debug(f"QA saved to postgres: {qa}")
    finally:
        await consumer.stop()
        logger.debug("Consumer stopped")


if __name__ == "__main__":
    asyncio.run(update_postgres())
