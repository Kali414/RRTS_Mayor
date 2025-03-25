from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

Mongo_URL=os.getenv("Mongo_URL")

client=MongoClient(Mongo_URL)

db=client["Practice_1"]

mayor=db["Mayor"]
issues=db["Issues"]
complaint=db["Complaints"]