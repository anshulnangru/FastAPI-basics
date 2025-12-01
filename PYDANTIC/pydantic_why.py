from pydantic import BaseModel, EmailStr, Field, AnyUrl
from typing import List,Dict,Optional

class Student(BaseModel):

    age:int=Field(gt=12,lt=30)
    name:str='anshul'
    email: EmailStr
    subjects: List[str]
    linkedIn: Optional[AnyUrl]=None
    marks:Dict[str,int]

def Student_Details(student: Student):
    
    print(student.age)
    print(student.marks)
    print(student.linkedIn)
    print(student.email)

data_entry={'age':'29','email':'anshul@gmail.com','subjects':['maths','hindi'],'linkedIn':'https://www.linkedin.com/in/anshul-nangru/','marks':{'maths':123,'english':1}}

s=Student(**data_entry)

Student_Details(s)


