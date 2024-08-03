# db.py
from pymongo import MongoClient
from config.config import settings

client = MongoClient(settings.DATABASE_URL)
db = client[settings.DATABASE_NAME]
