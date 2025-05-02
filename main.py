from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import quizquestionroute

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://quiz-app-frontend-ovgx-1f3wzd9v5-preraks-projects-7de96907.vercel.app"],
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
)


app.include_router(quizquestionroute.router , prefix="/quiz" , tags=["Quiz"])

