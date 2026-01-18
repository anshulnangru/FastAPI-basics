from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel, Field
from typing import Annotated, Optional
from random import randrange
import psycopg
import time
from psycopg.rows import dict_row
class Student(BaseModel):
   #id:Annotated[Optional[int],Field(description="id of the student")]
    name:Annotated[str,Field(...,description="name of the student")]
    course:Annotated[str,Field(...,description="course of the student")]
    

app = FastAPI()

while True:
    try:
        conn=psycopg.connect(
            host="localhost",
            port=5432,
            dbname="fastapi",     
            user="postgres",
            password="postgres" ,
            row_factory=dict_row
        )
        cursor=conn.cursor()
        print("Database connection was succesfull!!")
        break
    except Exception as error:
        print("Connectin to databse failed")
        print("error: ",error)
        time.sleep(2)
@app.get("/")
def root():
    return {"message" : "hello world"}

students =[{
    "id":103,
    "name":"nishant",
    "course":"bca",
        },
   {
    "id":104,
    "name":"anshul",
    "course":"bca",
        }
]

@app.get("/data")
def data():
    cursor.execute("SELECT * FROM public.students;")
    students=cursor.fetchall()
    return {"student_info" : students}

def find_student(id):
    for s in students:
        if s["id"]==id:
            return s
        

def find_index_student(id):
    for i,p in enumerate(students):
        if p['id']==id:
            return i

@app.post("/ent_st",status_code=status.HTTP_201_CREATED)
def create_student(student : Student):
    cursor.execute(""" INSERT INTO students (name, course) VALUES (%s,%s) RETURNING * """,(student.name,student.course))
    
    new_student=cursor.fetchone()
    conn.commit()

    return {"student_info" : new_student}

@app.get("/get_student/{id}")
def get_student(id: int, response:Response):

    cursor.execute("""SELECT * from students where id = %s""",(id, ))
    student=cursor.fetchone()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} was not found')
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {'message':f'post with id: {id} was not fount'}


    
    return {"the student with the given id is": student}

@app.delete("/delete_student/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(id: int):
    
    cursor.execute(""" DELETE FROM students where id=%s RETURNING *""",(id,))
    deleted_psot=cursor.fetchone()
    conn.commit()

    if deleted_psot==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Student with id {id} does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/update_student/{id}")
def update_student(id : int,student : Student):
    cursor.execute("""UPDATE students SET name = %s, course = %s where id = %s RETURNING *""",(student.name,student.course, str(id)))
    updated_student=cursor.fetchone()
    conn.commit()
    if updated_student==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Student with id {id} does not exist")
    
    return {'data': updated_student}