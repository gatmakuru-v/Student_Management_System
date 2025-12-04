from bson import ObjectId
from database import student_collection, user_collection
from utils import hash_password


async def create_user(username: str, password: str):
    if await user_collection.find_one({"username": username}):
        return None
    hashed = hash_password(password)
    await user_collection.insert_one({"username": username, "password": hashed})
    return {"username": username}

async def get_user(username: str):
    return await user_collection.find_one({"username": username})


def student_helper(student) -> dict:
    return {
        "id": str(student["_id"]),
        "name": student["name"],
        "age": student["age"],
        "course": student["course"],
        "email": student["email"],
        "phone": student["phone"],
        "address": student["address"],
        "enrollment_date": student["enrollment_date"],
        "is_active": student["is_active"],
    }

async def create_student(data: dict):
    student = await student_collection.insert_one(data)
    new_student = await student_collection.find_one({"_id": student.inserted_id})
    return student_helper(new_student)

async def get_all_students():
    students = []
    async for student in student_collection.find():
        students.append(student_helper(student))
    return students

async def get_student(student_id: str):
    student = await student_collection.find_one({"_id": ObjectId(student_id)})
    if student:
        return student_helper(student)

async def update_student(student_id: str, data: dict):
    if len(data) < 1:
        return False
    result = await student_collection.update_one(
        {"_id": ObjectId(student_id)},
        {"$set": data}
    )
    if result.modified_count:
        updated = await student_collection.find_one({"_id": ObjectId(student_id)})
        return student_helper(updated)
    return False

async def delete_student(student_id: str):
    result = await student_collection.delete_one({"_id": ObjectId(student_id)})
    return result.deleted_count == 1
