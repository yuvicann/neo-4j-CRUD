from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from neo4j_wrapper import Neo4jWrapper
import neo4j_wrapper

app = FastAPI()

# Neo4j connection
neo4j = Neo4jWrapper(uri="bolt://localhost:7687", user="neo4j", password="ahd@LUS#255")

# Define the Student model
class Student(BaseModel):
    id: str
    name: str
    age: int
    grade: str

# Create a student
@app.post("/students/")
def create_student(student: Student):
    response = neo4j.create_student(student.id, student.name, student.age, student.grade)
    if not response:
        raise HTTPException(status_code=400, detail="Student could not be created")
    return {"message": "Student created successfully", "student": response}

# Read a student
@app.get("/students/{student_id}")
def get_student(student_id: str):
    student = neo4j.get_student(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# Update a student
@app.put("/students/{student_id}")
def update_student(student_id: str, student: Student):
    response = neo4j.update_student(student_id, student.name, student.age, student.grade)
    if not response:
        raise HTTPException(status_code=400, detail="Student could not be updated")
    return {"message": "Student updated successfully", "student": response}

# Delete a student
@app.delete("/students/{student_id}")
def delete_student(student_id: str):
    response = neo4j.delete_student(student_id)
    if not response:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}

@app.get("/students/")
def get_all_students():
    students = neo4j.get_all_students()
    return students

# Close the Neo4j connection when the app shuts down
@app.on_event("shutdown")
def shutdown_event():
    neo4j.close()
