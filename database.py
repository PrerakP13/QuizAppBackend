import urllib.parse
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

# ✅ Encode the password correctly
password = urllib.parse.quote_plus("Prerak@13")  # Escapes special characters

# ✅ Use the encoded password in the connection string
MONGO_URI = f"mongodb+srv://prerakp87:{password}@cluster0.jb4qkao.mongodb.net/MyQuiz"

# ✅ Connect to MongoDB Atlas
client = AsyncIOMotorClient(MONGO_URI)
db = client["MyQuiz"]
questionbankdb = db["QuestionBank"]

print("Connected to MongoDB Atlas successfully!")  # ✅ Debugging confirmation

