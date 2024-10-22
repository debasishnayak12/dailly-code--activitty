from fastapi import FastAPI,Depends,HTTPException,Form,UploadFile,File
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import engine,get_db
from models import User as modeluser
from typing import Optional
import uvicorn 
from fastapi.middleware.cors import CORSMiddleware
import os
import numpy as np
from datetime import datetime

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# models.Base.metadata.create_all(bind=engine)


def validate_data(user,db):
    if 'name' not in user or  user['name'].isdigit() or  user['name']=="":
        return "Enter a valid Name"
    if 'email' not in user or  "@" not in str(user['email']) or "." not in str(user["email"]) or user.get('email')=="":
        return "Enter a valid email"
    if 'mobile' not in user or not user['mobile'].isdigit() or not len(str(user["mobile"]))==10 or user.get('mobile')=="" or (user['mobile'])[0]=='0':
        return "Enter a valid Mobile number"
    existing_user = db.query(modeluser).filter(modeluser.email == user["email"]).first()
    existing_mobile = db.query(modeluser).filter(modeluser.mobile == user["mobile"]).first()
    if existing_user:
        return "User Email Already Exist"
    # Check if the mobile number already exists
    if existing_mobile:
        return "Mobile Already Exist"
    return None


allowed_extensions=['png','jpg','jpeg','gif']
def check_file_extension(filename):
    if '.' not in filename or filename.rsplit('.',1)[1].lower() not in allowed_extensions:
        response={'response':'false','message':'UnSupported FileType!'}
        return (response),
# create user 
# Goes up to 'adminpanel\modules\user'
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  
# Path to 'adminpanel\modules\user\uploads'
UPLOAD_DIR = os.path.join(BASE_DIR, 'uploads')  

# Ensure the uploads directory exists
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)
    
@app.post("/users/add_user")
async def create_user(name:str = Form(...),
                email:str=Form(...),
                mobile:str =Form(...),
                image:Optional[UploadFile] = File(None),
                status:int = Form(...),
                db:Session = Depends(get_db)):
    final_user = {"name":name,"email":email,"mobile":mobile}
    validation_error = validate_data(final_user,db)
    if validation_error:
        response = {"response":"false","message":validation_error}
        return response
    try:
        
        image_path = None
        if image:
            file_name = image.filename
            file_extension = file_name.split('.')[1]
            rand = np.random.randint(1000,9999,1)
            current_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            File_Name = f"{current_time}_{rand[0]}.{file_extension}"
            check_file_extension(file_name)
            image_path = f"uploads/{File_Name}"
            save_path = os.path.join(UPLOAD_DIR, File_Name)  # Full path to save the image
            with open(save_path, "wb") as buffer:
                buffer.write(image.file.read())
                
        db_user = modeluser(name = name,email=email ,mobile = mobile ,image=image_path,status=status)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        response = {"response":"true","message":"Success"}
        return response
    except :
        response = {"response":"false","message":"Failed"}
        return response

#get_all_users
@app.post("/users/get_all")
async def get_users(showdatalimit: int = Form(...),
    currentpage: int = Form(...),
    name: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    mobile: Optional[str] = Form(None),
    db: Session = Depends(get_db)):
    statrfrom = (currentpage-1)*showdatalimit

    try:
        query = db.query(modeluser)
        
        if name:
            query = query.filter(modeluser.name.like(f'%{name}%'))
        if email:
            query = query.filter(modeluser.email.like(f'%{email}%'))
            
        if mobile:
            query = query.filter(modeluser.mobile.like(f'%{mobile}%'))
        query = query.order_by(modeluser.id.desc())
        users = query.offset(statrfrom).limit(showdatalimit).all()
        
        totalrows = db.query(func.count(modeluser.id)).scalar()

        ordered_result=[]
        for user in users:
            result = {
                "userid": user.id,
                "name": user.name,
                "email": user.email,
                "mobile": user.mobile,
                "imageurl": user.image,
                "status": user.status,
                "time":user.time
            }
            ordered_result.append(result)
                                 
        response = {"response":"true","message":"Success","user":ordered_result,"totalrows":totalrows}
        
        return response
    except :
        false_response = {"response":"false","message":"Failed"}
        return false_response
#get_one_data
@app.post("/users/get_one")
async def get_user(key:int=Form(...),db:Session = Depends(get_db)):
    user_id = key
    print(user_id)
    try:
        user = db.query(modeluser).filter(modeluser.id == user_id).first()
        print(db.query(modeluser).filter(modeluser.id == user_id))
        print(user.id,user.name,user.email,user.mobile,user.image,user.status,user.time)
        print(user)
        result ={
            "userid":user.id,
            "name":user.name,
            "email":user.email,
            "mobile":user.mobile,
            # "image":user.image,
            "status":user.status,
            # "time":user.time
            
        }
        if user is None:
            response = {"response":"false","message":"Failed","Error":"user id not found"}
            return response
        response = {"response":"true","message":"Success","user":result}
        return response
    except:
        response = {"response":"false","message":"Failed"}
#update user 
@app.post("/users/update")
async def user_update(
                userid:str =Form(...),
                name:str =Form(...),
                email:str = Form(...),
                mobile:str =Form(...),
                status:int = Form(...),
                db:Session=Depends(get_db)):
    check_user = db.query(modeluser).filter(modeluser.id!=userid).all()
 
    email_list = []
    mobile_list = []
    for user in check_user:
        emails = user.email
        mobiles=user.mobile
        email_list.append(emails)
        mobile_list.append(mobiles)
        
    if email in email_list:
        response = {"response":"false","message":"Email Already Used"}
        return response
    if mobile in mobile_list:
        response ={"response":"false","message":"Mobile Already Used"}
        
    try:
        user = db.query(modeluser).filter(modeluser.id ==userid).first()
        # print("user id :",id)
        user.name = name
        user.email=email
        user.mobile=mobile
        user.status = status
        db.commit()
        db.refresh(user)
        response = {"response":"true","message":"Success"}
        return response
    except:
        response = {"response":"false","message":"Failed"}
        return response
#user delete
@app.post("/users/delete",response_model=dict)
async def user_delete(key:int = Form(...),db:Session = Depends(get_db)):
    try:
        user = db.query(modeluser).filter(modeluser.id ==key).first()
        db.delete(user)
        db.commit()
        response = {"response":"true","message":"Success"}
        return response
    except:
        response={"response":"false","message":"Failed"}
        
    
if __name__=="__main__":
    uvicorn.run("main:app",host="localhost",port=5000,reload=True)
    

