from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.orm import Session 
import schemas,models
from database import engine,get_db
from models import User as modeluser
from schemas import User

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# create user 

@app.post("/users/add_user",response_model=dict)
def create_user(user:schemas.UserCreate,db:Session = Depends(get_db)):
    db_user = modeluser(name = user.name,email=user.email ,age = user.age)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    response = {"response":"true","message":"Success"}
    return response

#get_all_users
@app.post("/users/get_all")
def get_users(db : Session = Depends(get_db)):
    users = db.query(modeluser).all()
    
    response = {"response":"true","message":"Success","user":users}
    
    return response
#get_one_data
@app.post("/users/get_one")
def get_user(userrequest:schemas.Userrequest,db:Session = Depends(get_db)):
    user = db.query(modeluser).filter(modeluser.id == userrequest.id).first()
    if user is None:
        response = {"response":"false","message":"Failed","Error":"user id not found"}
        return response
    response = {"response":"true","message":"Success","user":user}
    return response
#update user 
@app.post("/users/update")
def user_update(user_update:schemas.UserUpdate,db:Session=Depends(get_db)):
    user = db.query(modeluser).filter(modeluser.id ==user_update.id).first()
    print("user id :",user_update.id)
    if user is None:
        raise HTTPException(status_code=404,detail = "user not found !")
    
    if user_update.name:
        user.name = user_update.name
        
    if user_update.email:
        user.email = user_update.email
        
    db.commit()
    db.refresh(user)
    response = {"response":"true","message":"Success"}
    return response

#user delete
@app.post("/users/delete",response_model=dict)
def user_delete(user_id:schemas.Userrequest,db:Session = Depends(get_db)):
    user = db.query(modeluser).filter(modeluser.id == user_id.id).first()
    if user is None:
        raise HTTPException(status_code = 404,detail = "user not Found")
    db.delete(user)
    db.commit()
    response = {"response":"true","message":"Success"}
    return response
        
    
    
    

