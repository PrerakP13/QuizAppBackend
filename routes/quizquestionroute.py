from bson import ObjectId
from fastapi import APIRouter, HTTPException
import logging
from database import get_collection
from models.quizCRUDmodel import QuizCollection
from models.quizquestionmodel import QuizSubmission, QuizBatchSubmission

router = APIRouter()

# ✅ Setup logging instead of print()
logging.basicConfig(level=logging.INFO)

# ✅ Fetch all existing questions
@router.get("/{quiz_name}")
async def get_quiz_questions(quiz_name: str):
    try:
        quiz_collection = await get_collection(quiz_name)

        if quiz_collection is None:
            raise HTTPException(status_code=404, detail=f"Quiz '{quiz_name}' not found.")

        questions = await quiz_collection.find({}, {"_id": 1, "question": 1, "options": 1, "correctAnswer": 1}).to_list(length=None)

        # ✅ Convert `_id` to string for frontend compatibility
        for q in questions:
            q["_id"] = str(q["_id"])

        return {"status": "success", "quiz_name": quiz_name, "questions": questions}

    except Exception as e:
        logging.error(f"Error fetching questions for '{quiz_name}': {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Route to update quiz questions
@router.put("/{quiz_name}/update")
async def update_quiz_questions(quiz_name: str, quiz_data: QuizBatchSubmission):
    try:
        quiz_collection = await get_collection(quiz_name)

        if quiz_collection is None:
            raise HTTPException(status_code=404, detail=f"Quiz '{quiz_name}' not found.")

        # ✅ Step 1: Delete all old questions
        await quiz_collection.delete_many({})

        # ✅ Step 2: Insert new updated questions
        new_questions = [q.model_dump() for q in quiz_data.questions]
        inserted = await quiz_collection.insert_many(new_questions)

        # ✅ Step 3: Log success & return response
        logging.info(f"Updated quiz '{quiz_name}' with {len(inserted.inserted_ids)} questions.")
        return {"status": "success", "message": f"Quiz '{quiz_name}' updated successfully!"}

    except Exception as e:
        logging.error(f"Error updating quiz batch for '{quiz_name}': {e}")
        raise HTTPException(status_code=500, detail=str(e))


    except Exception as e:
        logging.error(f"Error updating quiz batch for '{quiz_name}': {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Delete a specific question
@router.delete("/{quiz_name}/remove/{question_id}")
async def delete_question(quiz_name: str, question_id: str):
    try:
        quiz_collection = await get_collection(quiz_name)

        if quiz_collection is None:
            raise HTTPException(status_code=404, detail=f"Quiz '{quiz_name}' not found.")

        result = await quiz_collection.delete_one({"_id": question_id})

        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Question not found.")

        return {"status": "success", "message": "Question removed successfully!"}

    except Exception as e:
        logging.error(f"Error deleting question '{question_id}' from '{quiz_name}': {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{quiz_name}/submit")
async def submit_quiz(quiz_name: str, quiz_data: QuizSubmission):
    try:
        quiz_collection = await get_collection(quiz_name)

        if quiz_collection is None:
            raise HTTPException(status_code=404, detail=f"Quiz '{quiz_name}' not found.")

        # ✅ Fetch correct answers from the database
        questions = await quiz_collection.find({}, {"_id": 1, "correctAnswer": 1}).to_list(length=None)
        correct_answers = {str(q["_id"]): q["correctAnswer"] for q in questions}

        logging.info(f"Correct Answers: {correct_answers}")
        logging.info(f"User Responses: {quiz_data.responses}")

        # ✅ Calculate score
        score = sum(1 for response in quiz_data.responses if correct_answers.get(response.question_id) == response.user_answer)

        logging.info(f"Computed Score: {score}")

        return {
            "status": "success",
            "message": f"Quiz '{quiz_name}' submitted!",
            "score": score
        }

    except Exception as e:
        logging.error(f"Error submitting quiz '{quiz_name}': {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{quiz_name}/create")
async def create_quiz(quiz_name: str, quiz_data: QuizBatchSubmission):
    try:
        quiz_collection = await get_collection(quiz_name)

        if quiz_collection is None:
            raise HTTPException(status_code=404, detail=f"Quiz '{quiz_name}' not found.")

        # ✅ Add `_id` automatically for each new question
        questions_with_ids = [{**q.model_dump(), "_id": str(ObjectId())} for q in quiz_data.questions]

        # ✅ Insert new questions into MongoDB
        result = await quiz_collection.insert_many(questions_with_ids)

        return {
            "status": "success",
            "message": f"Quiz '{quiz_name}' created successfully!",
            "inserted_ids": [str(id) for id in result.inserted_ids]
        }

    except Exception as e:
        logging.error(f"Error creating quiz '{quiz_name}': {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{quiz_name}/remove/{questionId}")
async def delete_question(quiz_name:str, questionId: str):
    try:
        quiz_collection = await get_collection(quiz_name)

        if quiz_collection is None:
            raise HTTPException(status_code=404, detail=f"No '{quiz_name}' found!")

        result = await quiz_collection.delete_one({"_id":ObjectId(questionId)})

        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail=f"No question found")

        return{
            "status":"success",
            "message":f"Question '{questionId}' deleted successfully!"
        }



    except Exception as e:
        logging.error(f"Error deleting question '{questionId}' from '{quiz_name}': {e}")
        raise HTTPException(status_code=500, detail=str(e))
