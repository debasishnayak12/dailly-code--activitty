from fastapi import FastAPI,Depends,HTTPException ,Form ,UploadFile,File #for file uplaods
from sqlalchemy.orm import Session
# from sqlalchemy import func
from database import get_db
from  models import User as modeluser
from typing import Optional
import uvicorn 
# import schemas
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse,StreamingResponse
import os
import io
import zipfile
import numpy as np
import pandas as pd
from datetime import datetime
from pathlib import Path
import xlsxwriter


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
    if  (user["name"]).isdigit() or  user["name"]=="":
        return "Enter a valid Name"
    if "@" not in str(user["email"]) or "." not in str(user["email"]) or user["email"]=="":
        return "Enter a valid email"
    if user["mobile"] is not None:
        if  not len(str(user["mobile"]))==10 or user["mobile"]=="":
            return "Enter a valid Mobile number"
        existing_mobile = db.query(modeluser).filter(modeluser.mobile == user["mobile"]).first()
        # Check if the mobile number already exists
        if existing_mobile:
            return "Mobile Already Exist"
                
    existing_user = db.query(modeluser).filter(modeluser.email == user["email"]).first()
    if existing_user:
        return "User Email Already Exist"
    return None
    
## checking file extension 
allowed_extensions=['.png','.jpg','.jpeg','.gif']
def check_file_extension(filename):
    print("file type :",os.path.splitext(filename)[1])
    if not os.path.splitext(filename)[1] in allowed_extensions:
        response={'status':'false','message':'UnSupported FileType!'}
        return JSONResponse(content = response,status_code = 400)
    
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists

## set user with all data with  image or status as optional .
@app.post("/setuser")
async def setuser(name:str = Form(...),
                mobile:str=Form(...),
                email:str =Form(...),
                image:Optional[UploadFile] = File(None),
                status:Optional[int] = Form( 0 ),
                db:Session = Depends(get_db)):
    final_user = {"name":name,"email":email,"mobile":mobile,"image":image}
    # print("name :",final_user['name'],final_user['email'],final_user['mobile'],final_user['image'])
    validation_error = validate_data(final_user,db)
    if validation_error:
        response = {"status":"false","message":validation_error}
        return JSONResponse(content = response,status_code = 400)
    try:
        
        image_path = None
        print("image name :",image.filename)
        if image.filename != '':
            file_name = image.filename
            file_extension =os.path.splitext(file_name)[1]
            rand = np.random.randint(1000,9999,1)
            current_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            File_Name = f"{current_time}_{rand[0]}_img{file_extension}"
            check_file_extension(file_name)
            image_path = UPLOAD_DIR/File_Name
            # save_path = os.path.join(UPLOAD_DIR, File_Name)  # Full path to save the image
            with open(image_path, "wb") as buffer:
                buffer.write(await image.read())
                
        db_user = modeluser(name = name,mobile = mobile,email = email ,image=image_path,status = status)
        print("final user :",final_user)
        if db_user:
            db.add(db_user)
            print("added")
            db.commit() 
            db.refresh(db_user)
            response = {"status":"true","message":"Setuser Successfully"}
            statuscode = 201
            print("complete")
        else:
            response = {"status":"false","message":"Unable to set user at this moment ."}
            statuscode = 400
        return JSONResponse(content = response,status_code = statuscode)
    except :
        response = {"status":"false","message":"Failed"}
        return JSONResponse(content = response,status_code = 500)
        
## get one user based on user id 
@app.post('/getuser')
async def getuser(
                user_id:int=Form(0),
                db:Session=Depends(get_db)
                ):
    
    print("user id :",user_id)
    if user_id == 0:
        return JSONResponse(content={"status": "false", "message": "Please Enter user id ."}, status_code=400)
    try:
        db_user = db.query(modeluser).filter(user_id==modeluser.id).first()
        if db_user:
            ordered_user = {
                "userid":db_user.id,
                "name":db_user.name,
                "mobile":db_user.mobile,
                "email":db_user.email,
                "image":db_user.image,
                "inserttime":db_user.insert_time.isoformat() if db_user.insert_time else None,
                "updatetime":db_user.update_time.isoformat() if db_user.update_time else None,
            }

            # final_user = final_user.append(ordered_user)
            response = {"status":"true","message":"Getuser Successfully","user":ordered_user}
            statuscode = 200
        else:
            response = {"status":"false","message":"Sorry! No User found ."}
            statuscode = 404
        return JSONResponse(content=response,status_code=statuscode)
        # return response
    except Exception as e:
        response = {"status":"false","message":"Failed","error":f"{e}"}
        return JSONResponse(content=response,status_code=500)

###  Get all users 
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
                "updatetime":user.update_time.isoformat() if user.update_time else None,
            }
            final_user.append(ordered_user)

        response = {"status":"true","message":"Getusers Successfully","user":final_user}
        return JSONResponse(content=response,status_code=200)
        # return response
    except Exception as e:
        response = {"status":"false","message":"Failed","error":f"{e}"}
        return JSONResponse(content=response,status_code=500)
    
## get last  user 
@app.post('/get_lastuser')
async def last_user(db:Session=Depends(get_db)):
    try:
        db_user = db.query(modeluser).order_by(modeluser.id.desc()).first()
   
        user = {
            "id":db_user.id,
            "name":db_user.name,
            "mobile":db_user.mobile,
            "email":db_user.email,
            "image":db_user.image,
            "status":db_user.status,
            "insert_time":db_user.insert_time.isoformat() if db_user.insert_time else None,
            "update_time":db_user.update_time.isoformat() if db_user.update_time else None,

        }
        
        response = {"status":"true","message":"Get lastuser successfully ","user":user}
        
        return JSONResponse(content=response,status_code = 200)
    except Exception as e:
        response =  {"status":"false","message":"Failed","Error":f"{e}"}
        return JSONResponse(content=response,status_code = 400)
    
##set user status

@app.post('/setstatus')
async def setstatus(user_id:int=Form(...),
                    status:int=Form(0),
                    db:Session=Depends(get_db)):
    try:
        
        db_user = db.query(modeluser).filter(user_id==modeluser.id).first()
        # Example datetime string
        datetime_str = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        if db_user:
            db_user.status = status
            db_user.update_time = datetime_str
            db.commit()
            db.refresh(db_user)
            response = {"status":"true","messgae":"Status Updated Successfully"}
            status = 201
        else:
            response = {"status":"false","messgae":"Sorry no user found on this id ."}
            status = 400
        return JSONResponse(content=response,status_code=status)
    except Exception as e:
        response = {"status":"false","messgae":"Failed","error":f"e"}
        return JSONResponse(content=response,status_code=500)
    

##set image on id 
@app.post("/setimage")
async def create_user(uid:int = Form(...),  
                #image:Optional[UploadFile] = File(None),
                image:UploadFile = File(...),
                db:Session = Depends(get_db)):
    print("id",id)
    print(image)
    try:
        image_path = None
        if image.filename =='':
            return JSONResponse(content = {"status":"false","message":"Please Select Image"},status_code = 400)
        file_name = image.filename
        file_extension = os.path.splitext(file_name)[1]
        rand = np.random.randint(1000,9999,1)
        current_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        File_Name = f"{current_time}_{rand[0]}_img{file_extension}"
        print("file name :",file_name)
        check_file_extension(file_name)
        image_path = UPLOAD_DIR/File_Name
        # save_path = os.path.join(UPLOAD_DIR, File_Name)  # Full path to save the image
        with open(image_path, "wb") as buffer:
            buffer.write(await image.read())
            
        db_user = db.query(modeluser).filter(modeluser.id == uid).first()
        print(db_user)
        if db_user:
            db_user.image = image_path
            #db.add(db_user)
            db.commit()
            db.refresh(db_user)
            response = {"status":"true","message":"Setimage  Successfully"}
            status = 200
        else:
            response = {"status":"false","message":"user not found ."}
            status = 400
        return JSONResponse(content = response,status_code = status)
    except :
        response = {"status":"false","message":"Failed"}
        return JSONResponse(content = response,status_code = 500)
    

##get images as zip file (all images )
@app.post('/getimage')

async def getimage(db: Session = Depends(get_db)):
    try:
        # Fetch all users from the database
        db_user = db.query(modeluser).all()

        # Create an in-memory byte stream for the zip file
        zip_buffer = io.BytesIO()
        # Create a zip file in memory
        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:          
            for user in db_user:
                if user.image:
                    #image_path = os.path.join(UPLOAD_DIR, user.image)
                    image_path = user.image
                  
                    if os.path.isfile(image_path):  # Check if the file exists
                        with open(image_path, 'rb') as img_file:
                            image_data = img_file.read()
                            # Customize the filename in the zip
                            image_name = f"{user.id}_{user.name}.png"
                            zip_file.writestr(image_name, image_data)

        zip_buffer.seek(0)  # Reset the buffer pointer

        # Set headers to indicate a file download with the specified filename
        headers = {
            'Content-Disposition': 'attachment; filename="user_images.zip"'
        }

        # Return the zip file as a streaming response
        return StreamingResponse(zip_buffer, media_type='application/zip', headers=headers)
    except Exception as e:
        response = {"status": "false", "message": "Failed", "error": str(e)}
        return JSONResponse(content=response, status_code=500)
    
##download  all users details as xlsx file 
@app.post('/downloadusers')
async def downloadusers(db:Session=Depends(get_db)):
    try:
        all_users = []
        db_user = db.query(modeluser).all()
        for user in db_user:
            ordered_user = {
                "userid":user.id,
                "name":user.name,
                "mobile":user.mobile,
                "email":user.email,
                "image":user.image, 
                "inserttime":user.insert_time.isoformat() if user.insert_time else None,
            }
            all_users.append(ordered_user)
            
        df = pd.DataFrame(all_users, columns=["userid", "name", "mobile", "email", "image", "inserttime"])

        # Creating an Excel file in memory
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name="Users")
        
        output.seek(0)

        # Returning the Excel file as a response for download
        headers = {
            'Content-Disposition': 'attachment; filename="users.xlsx"'
        }

        response = StreamingResponse(output, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', headers=headers)

        response.headers["X-Message"] ="Success"
        response.headers["X-Status"] = "True"

        return response

    except Exception as e:
        response = {"status":"false","message":"Failed","error":f"{e}"}
        return JSONResponse(content=response,status_code=500)
    

# delete user 
@app.post('/deleteuser')
async def deleteuser(user_id:int = Form(0),db:Session=Depends(get_db)):
    if user_id == 0:
        response = {"status":"false","message":"Please Enter user id ."}
        return JSONResponse(content=response,status_code=400)
    try:
        db_user = db.query(modeluser).filter(user_id==modeluser.id).first()
        filepath = db_user.image 
        if os.path.exists(filepath):
            os.remove(filepath)
        if db_user:
            if db_user.image != '' or db_user.image!=None:
                filepath = db_user.image 
                if os.path.exists(filepath):
                    os.remove(filepath)
            db.delete(db_user)
            db.commit()
            response =  {"status":"true","message":"Successfully deleted ."}
            statuscode = 200
        else:
            response =  {"status":"false","message":"User does not exist ."}
            statuscode = 404
        
        return JSONResponse(content=response,status_code=statuscode)
        
    except :
        response = {"status":"false","message":"Failed to delete ."}
        return JSONResponse(content=response,status_code=500)
    

        
if __name__ =="__main__":
    uvicorn.run("main:app",port = 8080 ,reload=True)
