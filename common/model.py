from pydantic import BaseModel

class Question(BaseModel):
    question: str


class QuestionAnswer(BaseModel):
    question: str
    answer: str
    time:str