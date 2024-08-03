from fastapi import FastAPI
from pymongo import MongoClient
from config.config import settings
from routes.root import router as api_router
from db import db 
app = FastAPI()

# Initialize MongoDB client and database
client = MongoClient(settings.DATABASE_URL)
db = client[settings.DATABASE_NAME]

app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
