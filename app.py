from flask import Flask,render_template,request,jsonify,url_for
import mysql.connector
import os

app =Flask(__name__)

upload_folder  = 'static/uploads'
app.config['upload_folder'] = upload_folder
def db_connection():
    conn = mysql.connector.connect(
        host ="localhost",
        user = "root",
        passwd ="",
        db = "api_test"
    )
    return conn

@app.route('/')
def index():
    return render_template("index.html")
    
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)
@app.route('/postimage',methods=["POST"])
def postimage():
    if 'image' not in request.files:
        return jsonify({"Error":"NO file "}),400
    file = request.files['image']
    
    if file.filename =='':
        return jsonify({"error":"No file selected"}),400
    
    file_path = os.path.join(app.config['upload_folder'],file.filename)
    file.save(file_path)
    
    image_url = url_for('static',filename = 'uploads/'+file.filename, _external = True)
    
    try:
        conn = db_connection()
        cur = conn.cursor(dictionary=True)
        query = "insert into image_store(image) values(%s)"
        val = (image_url,)
        cur.execute(query,val)
        conn.commit()
        return jsonify({"Status":"True","message":"Insert data"}),200

    except mysql.connector.Error as e:
        return jsonify({"Status":"False","Message":f"{e}"})
    # with open(f"{request.form.get('name')}.txt" ,"w") as f:
    #     f.write("POST created ")
        

        
if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)