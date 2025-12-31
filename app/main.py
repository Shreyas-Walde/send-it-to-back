from typing import Optional, List
from fastapi import FastAPI, Response,status, HTTPException, Depends
from fastapi.params import Body

from random import randrange

import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db
from .routers import post, user


models.Base.metadata.create_all(bind=engine)

app = FastAPI() # instace of fastapi with function

while True:

    try:
        conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='koyo', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful!")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)


# example database

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "favorite foods", "content": "I like pizza", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i 


app.include_router(post.router)
app.include_router(user.router)

@app.get("/")    # decorator and read
#   get -> http method to read
def root():
    return {"message": "Hello Everynya how are yo?"}

# # for test
# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
    
#     posts = db.query(models.Post).all()  # every single entry in post table
#     return {"data": posts}



