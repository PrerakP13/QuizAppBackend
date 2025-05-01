from fastapi import APIRouter, HTTPException
from database import questionbankdb
from models.quizquestionmodel import QuizSubmission

router = APIRouter()

@router.get("/home")
async def get_quiz_questions():
    try:
        question = await questionbankdb.find({}, {"_id": 0, "question": 1, "options": 1}).to_list(length=None)
        return {"question": question}

    except Exception as e:
        print("Error fetching questions")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/submit")
async def handle_quiz_submit(quiz_data: QuizSubmission):
    try:
        questions = questionbankdb.find({}, {"_id":1, "correctAnswer":1}).to_list(length=None)
        correct_answers = {str(q["_id"]): q["correctAnswer"] for q in questions}

        score = sum(1 for response in quiz_data.responses if correct_answers[response.question_id]== response.user_answer)
        return {"message": "Quiz submission received!", "score":score}

    except Exception as e:
        print(f"Error handling quiz submission: {e}")
        raise HTTPException(status_code=500, detail=str(e))
