from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import quizquestionroute, userroute, quizCRUDroute
import sys
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://quiz-app-frontend-d4y9s3q8b-preraks-projects-7de96907.vercel.app"],
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
)


app.include_router(quizquestionroute.router , prefix="/quiz" , tags=["Quiz"])
app.include_router(userroute.router, prefix="/user", tags=["UserLogin"])
app.include_router(quizCRUDroute.router, prefix="/dashboard", tags=["QuizDashboard"])


print(sys.modules.get("datetime"))
