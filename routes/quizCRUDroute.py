from fastapi import APIRouter, HTTPException

from database import create_collection, get_quiz_collections, delete_collection, rename_collection
from models.quizCRUDmodel import QuizCollection

router = APIRouter()

@router.post("/add_new_quiz")
async def add_quiz(new_quiz: QuizCollection):
    try:
        await create_collection(new_quiz.QuizName)  # ✅ Calls function to create the collection

        return {
            "status": "success",
            "message": f"Quiz '{new_quiz.QuizName}' created successfully!",
            "quiz_name": new_quiz.QuizName
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
async def get_quizzes():
    try:
        quizlist = await get_quiz_collections()
        return {"status": "success","quizzes": quizlist}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete_quiz")
async def delete_quiz(quiz: QuizCollection):
    try:
        await delete_collection(quiz.QuizName)
        return {
            "status": "success",
            "message": f"Successfully deleted quiz '{quiz.QuizName}'"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/update_quiz/{quizName}")
async def update_quiz(quizName:str, newName: str):
    try:
        await rename_collection(quizName, newName)
        return {
            "status": "success",
            "message": f"Quiz '{quizName}' renamed to '{newName}'"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
