from pyexpat.errors import messages

from kafka import KafkaConsumer, KafkaProducer
from common.model import QuestionAnswer


def send_to_kafka(qa: QuestionAnswer,port="9092"):
    producer = KafkaProducer(bootstrap_servers=f'localhost:{port}')
    message = qa.model_dump_json().encode()
    producer.send("history", message)


def get_from_kafka(limit: int,port="9092") -> list[QuestionAnswer]:
    consumer = KafkaConsumer(
        'history',
        bootstrap_servers=f'localhost:{port}',
        auto_offset_reset = 'latest',
        group_id="my_group"
    )

    messages = []
    for message in consumer:
        qa = QuestionAnswer.model_validate_json(message.value.decode())
        messages.append(qa)
        if len(messages) == limit:
            break

    return messages
