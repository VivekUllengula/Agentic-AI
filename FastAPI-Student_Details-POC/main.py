from fastapi import FastAPI
from pydantic import BaseModel
import asyncio
import json
import os

#Getting the students data file directory
BASE_DIR = os.path.dirname(__file__)
FILE_PATH = os.path.join(BASE_DIR, "students.json")

#Loading students from json file to python dict
async def load_students():
    with open(FILE_PATH, "r") as f:
        return json.load(f)

#This is the ref pydantic student model
class Student(BaseModel):
    name: str
    age: int
    status: str

#Student services functions
async def get_all_students():
    students = await load_students()
    return students

async def get_a_student(name):
    students = await load_students()
    for s in students:
        if s["name"] == name:
            return s
        
async def add_a_student(student: Student):
    students = await load_students()
    student.status = student.status.lower()
    students.append(student.dict())

    with open(FILE_PATH, "w") as f:
        json.dump(students, f, indent=4)

    return student

async def get_active_students():
    students = await load_students()
    return [s for s in students if str(s.get("status", "")).strip().lower() == "active"]

#Fast API app initiation
app = FastAPI()

#GET / All students
@app.get('/students')
async def get_students():
    return await get_all_students()

#GET / Single student from name
@app.get('/students/{name}')
async def get_student(name: str):
    return await get_a_student(name)

#POST / Create a new student
@app.post('/students')
async def add_student(student: Student):
    return await add_a_student(student)

#GET / Get only active students
@app.get('/students/status')
async def active_students():
    return await get_active_students()
    