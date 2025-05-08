from pydantic import BaseModel


class QuizCollection(BaseModel):
    QuizName: str