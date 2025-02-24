from fastapi import FastAPI
from common.model import Question, QuestionAnswer
from common.ollama import *

import os
import sys
import logging

app = FastAPI()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(sys.stdout)
log_formatter = logging.Formatter(
    "%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s")
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)


@app.post("/question")
async def question(question: Question):
    answer = await ask_ollama(question.question)
    qa = QuestionAnswer(question=question.question, answer=answer)
    return qa
