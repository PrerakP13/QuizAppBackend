import urllib.parse
from motor.motor_asyncio import AsyncIOMotorClient


# ✅ Encode the password correctly
password = urllib.parse.quote_plus("Prerak@13")  # Escapes special characters

# ✅ Use the encoded password in the connection string
MONGO_URI = "mongodb+srv://prerakp87:Prerak%4013@cluster0.jb4qkao.mongodb.net"

# ✅ Connect to MongoDB Atlas with Motor (Auto-Handles SSL/TLS)
client = AsyncIOMotorClient(MONGO_URI)
db = client["MyQuiz"]

usersdb = db["Users"]

print("Connected to MongoDB Compass successfully!")  # ✅ Debugging confirmation

async def get_quiz_collections():
    try:
        collectionslist = await db.list_collection_names()
        filteredcollections = (col for col in collectionslist if col != "Users")
        return filteredcollections
    except Exception as e:
        raise Exception (f"Error fetching collections: '{str(e)}'")

async def get_collection(collection: str):
    try:

        return db.get_collection(collection)
    except Exception as e:
        raise Exception(f"No collection '{str(e)}' exists")

async def create_collection(collection_name: str):
    try:
        await db.create_collection(collection_name)  # ✅ MongoDB will create this if it doesn't exist

        return f"Collection '{collection_name}' created successfully!"
    except Exception as e:
        raise Exception(f"Error creating collection: {str(e)}")


async def delete_collection(collection_name:str):
    try:
        collection_instance = db.drop_collection(collection_name)
        return f"Collection '{collection_name}' deleted successfully!"
    except Exception as e:
        raise Exception(f"Error deleting collection:{str(e)}")


async def rename_collection(old_name: str, new_name: str):
    try:
        # ✅ Get the old collection
        old_collection = db.get_collection(old_name)

        # ✅ Create new collection & copy data
        new_collection = db.get_collection(new_name)
        documents = await old_collection.find().to_list(length=None)
        if documents:
            await new_collection.insert_many(documents)

        # ✅ Drop the old collection
        await old_collection.drop()

        return {"status": "success", "message": f"Collection '{old_name}' renamed to '{new_name}'"}

    except Exception as e:
        raise Exception(f"Error renaming collection: {str(e)}")