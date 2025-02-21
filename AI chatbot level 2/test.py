# from pymongo import MongoClient
# import os

# def test_mongodb_connection():
#     mongo_uri = "mongodb+srv://vasu:Omkarg535%40@moviechatbot.ktyku.mongodb.net/?retryWrites=true&w=majority&appName=moviechatbot"
    
#     try:
#         # Connect to MongoDB
#         client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        
#         # Check server connection
#         client.admin.command("ping")
#         print("✅ Successfully connected to MongoDB!")
        
#         # Create or check a test database
#         db_name = "test_db"
#         db = client[db_name]
        
#         # Create a test collection and insert a document
#         collection = db["test_collection"]
#         test_doc = {"message": "MongoDB connection successful!"}
#         collection.insert_one(test_doc)
        
#         print(f"✅ Database '{db_name}' and test collection created successfully!")
    
#     except Exception as e:
#         print("❌ MongoDB connection failed:", e)
#     finally:
#         client.close()
#         print("🔄 Connection closed.")

# if __name__ == "__main__":
#     test_mongodb_connection()


from database import get_dialogue

# Test if dialogue exists for "tony" with the message "who are you"
print(get_dialogue("tony", "who are you"))
