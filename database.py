from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.collection import Collection

mongo_uri = "mongodb://localhost:27017/"
db_name = "MyQuiz"

client = AsyncIOMotorClient('mongodb://localhost:27017')
db = client[db_name]

questionbankdb = db["QuestionBank"]