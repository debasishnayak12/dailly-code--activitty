from fastapi import FastAPI,Depends,HTTPException ,Form #,UploadFile,File for file uplaods
from sqlalchemy.orm import Session
# from sqlalchemy import func
from database import get_db
from  models import User as modeluser
# from typing import Optional
import uvicorn 
import schemas
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
# import numpy as np
from datetime import datetime


# models.Base.metadata.create_all(bind=engine)  #uncomment this to create table if not exists
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def validate_data(user,db):
    if  (user.name).isdigit() or  user.name=="":
        return "Enter a valid Name"
    if "@" not in str(user.email) or "." not in str(user.email) or user.email=="":
        return "Enter a valid email"
    if user.mobile is not None:
        if  not len(str(user.mobile))==10 or user.mobile=="":
            return "Enter a valid Mobile number"
        existing_mobile = db.query(modeluser).filter(modeluser.mobile == user.mobile).first()
        # Check if the mobile number already exists
        if existing_mobile:
            return "Mobile Already Exist"
                
    existing_user = db.query(modeluser).filter(modeluser.email == user.email).first()
    if existing_user:
        return "User Email Already Exist"
    return None
    

@app.post('/setuser')
async def CreateUser(user:schemas.UserCreate,db:Session = Depends(get_db)):
    try:
        db_user=modeluser(
            
            name=user.name,
            mobile=user.mobile , # for optional add (if user.mobile else None)
            email=user.email
            
        )
        validation_error=validate_data(user,db)
        if validation_error:
            response =  {"status":"false","message":validation_error}
            return JSONResponse(content=response,status_code=400)
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        response = {"status":"true","message":"Inserted Succeessfully"}
        return JSONResponse(content=response,status_code=201)
    except Exception as e:
        response = {"status":"false","message":"Failed","error":f"{e}"}
        return JSONResponse(content=response,status_code=500)
        

@app.post('/getuser')
async def getuser(
                user_id:int=Form(...),
                db:Session=Depends(get_db)
                ):
    userid=user_id
    print("user id :",user_id)
    if userid is None:
        return JSONResponse(content={"status": "false", "message": "User not found"}, status_code=404)
    try:
        db_user = db.query(modeluser).filter(userid==modeluser.id).first()
        # db_user = db.query(modeluser).all()
        print("user id :",user_id)
        # final_user = []
        ordered_user = {
            "userid":db_user.id,
            "name":db_user.name,
            "mobile":db_user.mobile,
            "email":db_user.email,
            "image":db_user.image,
            "inserttime":db_user.insert_time.isoformat() if db_user.insert_time else None,
        }

        # final_user = final_user.append(ordered_user)
        response = {"status":"true","message":"Getuser Successfully","user":ordered_user}
        return JSONResponse(content=response,status_code=200)
        # return response
    except Exception as e:
        response = {"status":"false","message":"Failed","error":f"{e}"}
        return JSONResponse(content=response,status_code=500)


@app.post('/getusers')
async def getusers(db:Session=Depends(get_db)):
    try:
    
        db_user = db.query(modeluser).all()
        final_user = []
        for user in db_user:

            ordered_user = {
                "userid":user.id,
                "name":user.name,
                "mobile":user.mobile,
                "email":user.email,
                "image":user.image,
                "inserttime":user.insert_time.isoformat() if user.insert_time else None,
            }
            final_user.append(ordered_user)

        response = {"status":"true","message":"Getusers Successfully","user":final_user}
        return JSONResponse(content=response,status_code=200)
        # return response
    except Exception as e:
        response = {"status":"false","message":"Failed","error":f"{e}"}
        return JSONResponse(content=response,status_code=500)
        
if __name__ =="__main__":
    uvicorn.run("main:app",port = 8080 ,reload=True)
