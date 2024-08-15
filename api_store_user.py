from flask import Flask,request,jsonify
import mysql.connector

app=Flask(__name__)
def db_connection():
    conn=mysql.connector.connect(
        host= "localhost",
        user="root",
        passwd="",
        database="imagecapture"
    )
    if conn :
        print("Connect successfully !")
    return conn

@app.route('/add_details',methods=["POST"])
def add_dettails():
    
    
    Name=request.form.get('Name')
    email=request.form.get('email')
    Mobile=request.form.get('Mobile')
    
    print("Name :",Name)
    print("email :",email)
    print("MOb :",Mobile)
    
    try:
        conn=db_connection()
        cur=conn.cursor()
        cur.execute('INSERT INTO photobooth (Name,email,Mobile) values (%s,%s,%s)',(Name,email,Mobile))
        conn.commit()
        inserted_id = cur.lastrowid
        conn.close()
        
        response = {"Status": "True", "Message": "Data inserted successfully", "id": inserted_id}
        print("Server response:", response)  # Debugging print
        return jsonify(response), 201
    except :
        return jsonify({"Status": "False", "Message": "Unable to insert data at this moment"}), 500
        
        
        
if __name__=="__main__":
    app.run(debug=True)


