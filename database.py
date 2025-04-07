from pymongo import MongoClient

import os
from dotenv import load_dotenv
load_dotenv()

Mongo_URL=os.getenv("MONGO_URL")
client=MongoClient(Mongo_URL)

db=client["Practice_1"]
resident=db["Residents"]
supervisor=db["Supervisor"]
city_admin=db["City_admin"]
mayor=db["Mayor"]
complaint=db["Complaints"]
issues=db["Issues"]
