from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from common.model import QuestionAnswer
import logging
import os
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(sys.stdout)
log_formatter = logging.Formatter(
    "%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] "
    "[%(levelname)s] %(name)s: %(message)s"
)
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)

KAFKA_ENDPOINT = os.getenv(
    "KAFKA_ENDPOINT", "localhost:29092"
)
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


async def get_from_kafka(limit: int) -> list[QuestionAnswer]:
    consumer = AIOKafkaConsumer(
        "history",
        bootstrap_servers=KAFKA_ENDPOINT,
        consumer_timeout_ms=500,
        enable_auto_commit=False,
        group_id="my_group",
    )

    messages = []
    await consumer.start()
    logger.info("Consumer started")
    try:
        async for message in consumer:
            logger.info("Message received from kafka")
            qa = QuestionAnswer.model_validate_json(message.decode())
            messages.append(qa)
            if len(messages) == limit:
                break
    finally:
        await consumer.stop()

    return messages
