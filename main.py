from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import quizquestionroute, userroute, quizCRUDroute
import sys
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://vercel.com/preraks-projects-7de96907/quiz-app-frontend/8NuCgCgY1reiCqw6QqDPbLRiR9p4","http://localhost:5173"],
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
)


app.include_router(quizquestionroute.router , prefix="/quiz" , tags=["Quiz"])
app.include_router(userroute.router, prefix="/user", tags=["UserLogin"])
app.include_router(quizCRUDroute.router, prefix="/dashboard", tags=["QuizDashboard"])



