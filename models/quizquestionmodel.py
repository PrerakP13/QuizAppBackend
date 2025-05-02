from pydantic import BaseModel, Field
from typing import List, Optional

class Question(BaseModel):
    _id: Optional[str]  # ✅ Allows optional MongoDB ID for new questions
    question: str = Field(..., min_length=5)  # ✅ Enforce valid length
    options: List[str] = Field(..., min_items=2)  # ✅ Prevents empty options lists
    correctAnswer: str = Field(...)

class QuestionResponse(BaseModel):
    question_id: str
    user_answer: str

class QuizSubmission(BaseModel):
    user_id: str
    responses: List[QuestionResponse]

class QuizBatchSubmission(BaseModel):
    questions: List[Question]