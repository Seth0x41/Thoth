from ast import Not
import imp
import sqlite3
import uvicorn
import requests
from fastapi import FastAPI, Query,Form,File,UploadFile
import sqlite3
from typing import List
import os
import aiofiles
import shutil
import bcrypt
import re


app = FastAPI()

def create_connection(db_file):
    """ Sqlite Database Connecting"""
    global db
    db = None
    try:
        db = sqlite3.Connection(db_file)
        print(f"Database Connected!")

    except Exception as e:
        print(f"Database Error: {e}")
    return db
    

@app.get("/")
def read_root():
    return {"Hello": "Worfldd"}

conn =create_connection("Telegrambot.sqlite")
cur = conn.cursor()

@app.post("/api/wake-up/{text}")
async def wake_up(text:str):
    query= cur.execute("SELECT chat_id from students")
    for chat_id in query.fetchall():
        url_req = "https://api.telegram.org/bot" + "TOKEN" + "/sendMessage" + "?chat_id=" + str(chat_id[0]) + "&text=" + text 
        requests.get(url_req)
    return {"msg":"success"}


@app.get("/api/fetch-all")
async def fetch_all():

    query = cur.execute("SELECT students.full_name, students.chat_id, students.student_level, department.department_name from students INNER JOIN department ON department.department_id = students.dapartment_id;")
    students=[
        dict(full_name=row[0],chat_id=row[1],student_level=row[2],department_name=row[3])
        for row in query.fetchall()
    ]
    return students


@app.get("/api/get-courses")
async def get_courses():

    query=cur.execute("SELECT course_id,course_name FROM courses")
    course_name=[dict(course_id=row[0],course_name=row[1]) for row in query.fetchall()]
    # courses = await database.fetch_all(query=query)
    return course_name

@app.get("/api/get-departments")
async def get_departments():
    query = cur.execute("SELECT department_id, department_name FROM department")
    department=[dict(department_id=row[0],department_name=row[1]) for row in query.fetchall()]
    return department


@app.get("/api/get-lectures")
async def get_lectures(id:int):
    query=cur.execute(f"SELECT course_name FROM courses WHERE course_id=?",(id,))
    [course_name]=query.fetchone()
    course_path=os.getcwd()+"\\"+"courses"+"\\"+course_name
    lectures=os.listdir(course_path)
    return dict(enumerate(lectures,1))

@app.post("/api/add-course/")
async def add_course(course_name:str = Form(...),related_departments:str= Form(...)):
    departments_id = [int(number) for number in related_departments.split(",")]
    try:
        cur.execute(f"INSERT INTO courses(course_name) VALUES ('{course_name}')")
        db.commit()
        query = cur.execute(f"SELECT course_id FROM courses WHERE course_name='{course_name}'")
        [course_id]=query.fetchone()
        for id in departments_id:
            cur.execute("INSERT INTO department_courses(course_id,department_id) VALUES (?,?)",(course_id,id))
            db.commit()
        path = "courses\\"+course_name.capitalize()
        # Create course directory
        if not os.path.exists(path):
            os.makedirs(path)
        return {"msg":"Course Added"}
    except Exception as e:
        if "UNIQUE" in str(e):
            return {"msg","This course already exist"}



@app.delete("/api/delete-course/")
async def delete_course(id=Form(...)):
    try:
        query=cur.execute(f"SELECT course_name FROM courses WHERE course_id=?",(id,))
        [course_name]=query.fetchone()
        cur.execute(f"DELETE FROM courses WHERE course_id=?",(id,))
        db.commit()
        location = "courses\\"
        dir = course_name.capitalize()
        path = os.path.join(location,dir)
        if os.path.exists(path):
            shutil.rmtree(path)
            return {"msg":"Course Deleted"}
    except Exception as e:
        return {"msg":e}

@app.post("/api/upload-lecture")
async def upload_lecture(course_id:int=Form(...),lecutre_name:str=Form(...),files: List[UploadFile] =File(...)):
    query=cur.execute(f"SELECT course_name FROM courses WHERE course_id=?",(course_id,))
    [course_name]=query.fetchone()
    location = "courses\\"
    dir = course_name.capitalize()
    path = os.path.join(location,dir,lecutre_name.capitalize())
    if not os.path.exists(path):
        os.makedirs(path)
    for file in files:
        async with aiofiles.open(f"{path}\\{file.filename}", 'wb') as out_file:
            content = await file.read()  # async read
            await out_file.write(content)  # async write
    return {"file_name": file.filename}
        
@app.delete("/api/delete-lecture")
async def delete_lecture(course_id:int=Form(...), lecture_name:str=Form(...)):
    query=cur.execute(f"SELECT course_name FROM courses WHERE course_id=?",(course_id,))
    [course_name]=query.fetchone()
    location = "courses\\"
    path = os.path.join(location,course_name,lecture_name)
    if os.path.exists(path):
        shutil.rmtree(path)
        return {"msg":"Course Deleted"}
    return {"msg":"something wrong"}



@app.post("/api/login")
async def login(username:str=Form(...), password:str=Form(...)):
    query=cur.execute(f"SELECT username,password FROM admin")
    data= query.fetchall()
    usr=data[0][1]
    user_password=data[0][1]
    salt = bcrypt.gensalt()
    if bcrypt.checkpw(password.encode('utf-8'), user_password):
        return {"msg":"redirect"}
    else:
        return {"msg:":"Wrong username or password."}
@app.put("/api/edit-user")
async def edit_user(*,username:str=None, password:str, confirm_password:str):
    if len(password) > 7 and password == confirm_password:
        hashed_pass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cur.execute(f"UPDATE admin SET password = ?",(hashed_pass,))
        db.commit()

    else:
        return {"msg": "password length must be more than 6 characters"}

    if username is not None and len(username.strip()) > 4:
        if re.match("^[a-zA-Z0-9_.-]+$",username):
            cur.execute(f"UPDATE admin SET username = ?",(username,))
            db.commit()
        else:
            return {"msg": "username length must be more than 4 characters."}

    return {"msg":"Updated"}

if __name__ == "__main__":
    uvicorn.run("main:app", debug=True, reload=True)
    create_connection("Telegrambot.sqlite")
