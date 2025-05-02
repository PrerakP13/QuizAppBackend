from fastapi import APIRouter, HTTPException
from database import questionbankdb
from models.quizquestionmodel import QuizSubmission, QuizBatchSubmission

router = APIRouter()


@router.get("/home")
async def get_quiz_questions():
    try:
        questions = await questionbankdb.find({}, {"_id": 1, "question": 1, "options": 1}).to_list(length=None)

        # Convert `_id` to string for frontend compatibility
        for q in questions:
            q["_id"] = str(q["_id"])

        return {"questions": questions}

    except Exception as e:
        print("Error fetching questions:", e)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/submit")
async def handle_quiz_submit(quiz_data: QuizSubmission):
    try:
        questions = await questionbankdb.find({}, {"_id": 1, "correctAnswer": 1}).to_list(length=None)
        correct_answers = {str(q["_id"]): q["correctAnswer"] for q in questions}

        print(f"Correct Answers: {correct_answers}")  # ✅ Debugging log
        print(f"User Responses: {quiz_data.responses}")  # ✅ Debugging log

        score = sum(1 for response in quiz_data.responses if correct_answers.get(response.question_id) == response.user_answer)

        print(f"Computed Score: {score}")  # ✅ Debugging log
        return {"message": "Quiz submitted successfully!", "score": score}

    except Exception as e:
        print(f"Error handling quiz submission: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/create-quiz-batch")
async def create_quiz_batch(quiz_data: QuizBatchSubmission):
    try:
        # ✅ Insert multiple questions into MongoDB
        result = await questionbankdb.insert_many([q.model_dump() for q in quiz_data.questions])

        return {"message": "Quiz batch created successfully", "inserted_ids": [str(id) for id in result.inserted_ids]}

    except Exception as e:
        print(f"Error creating quiz batch: {e}")
        raise HTTPException(status_code=500, detail=str(e))

