from flask import Flask,request,jsonify
import os
from werkzeug.utils import secure_filename

app=Flask(__name__)

upload_folder='upload_images'
app.config['upload_folder']=upload_folder

os.makedirs(upload_folder,exist_ok=True)

allowed_extensions={"png","jpg","jpeg","gif"}

def allowed_filename(filename):
    return '.' in filename and filename.split('.' ,1)[1].lower() in allowed_extensions

@app.route('/UploadImages',methods=["POST"])
def upload_image():
    file=request.files['file']
    print("Request Files:", request.files)
    print("Request Form:", request.form)
    if 'file' not in request.files:
        return jsonify({"Status":"False","Message": "No file part detected"}), 400
    
    if file.filename=='':
        return jsonify({"Status":"False","Message":"NO file selected to uplaod "})
    
    if file and allowed_filename(file.filename):
        filename=secure_filename(file.filename)
        directory=request.form.get("directory",'')
        if not directory:
            return jsonify({"Status":"False","Message": "Directory not specified"}), 400
        
        directory_path=os.path.join(app.config['upload_folder'],directory)
        os.makedirs(directory_path,exist_ok=True)
        file_path=os.path.join(directory_path,filename)
        file.save(file_path)
        return jsonify({"Status ":"True ","Message":f"File uploaded successfully to : {file_path}"}),200
    return jsonify({"Status":"False","Message":"Invalid filetype"}),400

if __name__=="__main__":
    app.run(debug=True)
