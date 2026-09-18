from fastapi import FastAPI 
from typing import Optional
from pydantic import BaseModel


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}   


@app.get("/greet")
def read_greet():
    return {"Hello": "greet"}   


#  with parameter 
@app.get("/greet/{name}")
def greet_name(name: str):
    return {"Hello": f"{name}"}

# http://127.0.0.1:8000/greets/tom?age=30

@app.get("/greets/{name}")
def greet_names(name: str, age: int):
    return {"Message: Hello": f"{name}", "Age": age}


@app.get("/preety/{name}")
def greet_names(name: str, age: Optional[int] = None):
    return {"Message: Hello": f"{name}", "Age": age}

# post api 

class Student (BaseModel):
    name: str 
    age: int 
    roll: int 

@app.post("/create_student")
def create_student(student: Student):
    return {
        "name": student.name,
        "age": student.age,
        "roll": student.roll
    }



