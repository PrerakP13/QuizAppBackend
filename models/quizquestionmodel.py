from pydantic import BaseModel
from typing import Optional

class Question (BaseModel):
    _id: str
    question : str
    options : list[str]
    correctAnswer : str

class QuestionResponse (BaseModel):
    question_id: str
    user_answer : str

class QuizSubmission (BaseModel):
    user_id: str
    responses : list[QuestionResponse]