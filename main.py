from fastapi import FastAPI,Depends,HTTPException #Form,UploadFile,File for file uplaods
from sqlalchemy.orm import Session
# from sqlalchemy import func
from database import get_db
from  models import User as modeluser
# from typing import Optional
import uvicorn 
#import schemas
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse,FileResponse,StreamingResponse
import io
import os
# import numpy as np
import zipfile
import pandas as pd
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



        
@app.post('/getuser')
async def getuser(db:Session=Depends(get_db)):
    # userid=user.id
    # if userid is None:
    #     return JSONResponse(content={"status": "false", "message": "User not found"}, status_code=404)
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
        print(df)
        #df.to_excel("users.xlsx")
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
        
# this is not workng here bcz no uploads folder here ...try this in base 3
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
if __name__ =="__main__":
    uvicorn.run("main:app",port = 8080 ,reload=True)
