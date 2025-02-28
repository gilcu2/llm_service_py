import logging
import os
import sys

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer  # type: ignore[import-untyped]

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

KAFKA_ENDPOINT = os.getenv("KAFKA_ENDPOINT", "localhost:9092")
logger.debug(f"kafka enpoint: {KAFKA_ENDPOINT}")


async def send_to_kafka(qa: QuestionAnswer):
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_ENDPOINT)
    await producer.start()
    try:
        message = qa.model_dump_json().encode()
        await producer.send_and_wait("history", message)
        logger.info("Message sent to kafka")
    finally:
        # Wait for all pending messages to be delivered or expire.
        await producer.stop()


async def get_from_kafka(
    group_id: str = "my_group", limit: int | None = None
) -> list[QuestionAnswer]:
    consumer = AIOKafkaConsumer(
        "history",
        bootstrap_servers=KAFKA_ENDPOINT,
        auto_offset_reset="earliest",
        group_id=group_id,
    )

    r = []
    await consumer.start()
    logger.info("Consumer started")
    try:
        data = await consumer.getmany(timeout_ms=1000, max_records=limit)
        for _, messages in data.items():
            for message in messages:
                qa = QuestionAnswer.model_validate_json(message.value.decode())
                r.append(qa)
    finally:
        await consumer.stop()

    return r
