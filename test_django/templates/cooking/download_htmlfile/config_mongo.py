from pymongo import MongoClient

client = MongoClient("localhost", port=27017)

mon_db = client["mYbOOKs"]

message = mon_db["message"]

message.insert_one(
    "message"
)

data = message.find()

for row in data:
    print(f"{row}")


























