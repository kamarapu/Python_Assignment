from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId
from typing import Optional

app = FastAPI()

# MongoDB connection
client = MongoClient("<mongodb_connection_string>")
db = client["user_profiles"]
collection = db["users"]

class User(BaseModel):
    id: Optional[str]
    name: str
    age: Optional[int]
    email: Optional[str]
    address: Optional[str]

# Endpoint to update user details
@app.put("/users/{user_id}")
def update_user(user_id: str, user: User):
    # Find the user by ObjectId
    existing_user = collection.find_one({"_id": ObjectId(user_id)})
    if existing_user:
        # Update user with new details
        user_data = user.dict(exclude_unset=True)  # Exclude unset fields from the request
        collection.update_one({"_id": existing_user['_id']}, {"$set": user_data})
        return {"message": "User details updated successfully"}

    return {"message": "User not found"}







@app.post("/upload-profile-picture/")
async def upload_profile_picture(profile_picture: UploadFile = File(...)):
    contents = await profile_picture.read()
    with open("uploaded_images/" + profile_picture.filename, "wb") as file:
        file.write(contents)
    return {"message": "Profile picture uploaded successfully"}


@app.put("/users/{user_id}")
def update_user(user_id: int, user: User):
    for existing_user in users:
        if existing_user.id == user_id:
            existing_user.name = user.name
            existing_user.age = user.age
            existing_user.email = user.email
            existing_user.address = user.address
            return {"message": "User details updated successfully"}

    return {"message": "User not found"}