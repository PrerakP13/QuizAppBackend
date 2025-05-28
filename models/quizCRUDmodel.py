from pydantic import BaseModel


class QuizCollection(BaseModel):
    quizName: str

