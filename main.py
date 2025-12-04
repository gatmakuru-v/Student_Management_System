from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
import crud
from models import UserCreate, Student, StudentUpdate
from utils import verify_password, create_access_token
from auth import get_current_user

app = FastAPI(title="Student Management System with JWT")


@app.post("/signup")
async def signup(user: UserCreate):
    created = await crud.create_user(user.username, user.password)
    if not created:
        raise HTTPException(400, "Username already exists")
    return {"message": "User created successfully"}

@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user = await crud.get_user(form.username)
    if not user or not verify_password(form.password, user["password"]):
        raise HTTPException(401, "Invalid username or password")
    token = create_access_token({"sub": user["username"]})
    return {"access_token": token, "token_type": "bearer"}


@app.post("/students")
async def create_student(student: Student, user=Depends(get_current_user)):
    return await crud.create_student(student.dict())

@app.get("/students")
async def get_students(user=Depends(get_current_user)):
    return await crud.get_all_students()

@app.get("/students/{student_id}")
async def get_student(student_id: str, user=Depends(get_current_user)):
    student = await crud.get_student(student_id)
    if not student:
        raise HTTPException(404, "Student not found")
    return student

@app.put("/students/{student_id}")
async def update_student(student_id: str, data: StudentUpdate, user=Depends(get_current_user)):
    updated = await crud.update_student(student_id, data.dict(exclude_none=True))
    if not updated:
        raise HTTPException(404, "Student not found or nothing updated")
    return updated

@app.delete("/students/{student_id}")
async def delete_student(student_id: str, user=Depends(get_current_user)):
    deleted = await crud.delete_student(student_id)
    if not deleted:
        raise HTTPException(404, "Student not found")
    return {"message": "Student deleted successfully"}
