from fastapi import FastAPI, status, HTTPException, Response, Depends

from app.database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
from app.routers import users, auth, sales
from app import models




models.Base.metadata.create_all(bind=engine)
app = FastAPI()


app.include_router(users.router) 
app.include_router(auth.router)
app.include_router(sales.router)







@app.get('/')
def root(): #
    return {'message': 'updated the read only access'}

