# import logging
# import os
# import sys
#
# from common.model import QuestionAnswer
# from kafka import KafkaConsumer, KafkaProducer
#
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
# stream_handler = logging.StreamHandler(sys.stdout)
# log_formatter = logging.Formatter(
#      "%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d]"
#     "[%(levelname)s] %(name)s: %(message)s"
# )
# stream_handler.setFormatter(log_formatter)
# logger.addHandler(stream_handler)
#
# KAFKA_ENDPOINT = os.getenv("KAFKA_ENDPOINT", "localhost:9094")
# logger.debug(f"Kafkaendpoint: {KAFKA_ENDPOINT}")
#
#
# def send_to_kafka(qa: QuestionAnswer):
#     producer = KafkaProducer(bootstrap_servers=KAFKA_ENDPOINT)
#     message = qa.model_dump_json()
#     producer.send("history", message.encode())
#     logger.debug(f"KafkaSent: {message}")
#
#
# def get_from_kafka(limit: int, group: str = "my_group") -> list[QuestionAnswer]:
#     consumer = KafkaConsumer(
#         "history",
#         bootstrap_servers=KAFKA_ENDPOINT,
#         # auto_offset_reset = 'latest',
#         group_id=group,
#     )
#
#     messages = []
#     logger.debug(f"Begin receiving messages from Kafka")
#     for message in consumer:
#         qa = QuestionAnswer.model_validate_json(message.value.decode())
#
#         messages.append(qa)
#         logger.debug(f"Received: {qa}")
#         if len(messages) == limit:
#             break
#
#     return messages
