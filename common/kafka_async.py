from pyexpat.errors import messages

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from common.model import QuestionAnswer


async def send_to_kafka(qa: QuestionAnswer):
    producer = AIOKafkaProducer(
        bootstrap_servers='localhost:9094')
    await producer.start()
    try:
        message = qa.model_dump_json().encode()
        await producer.send_and_wait("history", message)
    finally:
        # Wait for all pending messages to be delivered or expire.
        await producer.stop()


async def get_from_kafka(limit: int) -> list[QuestionAnswer]:
    consumer = AIOKafkaConsumer(
        'history',
        bootstrap_servers='localhost:9094',
        consumer_timeout_ms=500,
        enable_auto_commit=False,
        group_id="my_group"
    )

    messages = []
    await consumer.start()
    print("Consumer started")
    try:
        async for message in consumer:
            qa=QuestionAnswer.model_validate_json(message.decode())
            messages.append(qa)
            if len(messages) == limit:
                break
    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()

    return messages