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

@app.route('/update_filename',methods=["POST"])
def update_filename():
    
    record_id=request.form.get('id')
    newfilename=request.form.get('filename')
    print("ID :",record_id)
    print("FIlename :",newfilename)
    try:
        conn=db_connection()
        cur=conn.cursor()
        cur.execute('SELECT * FROM photobooth where id=%s',(record_id,))
        record=cur.fetchone()
        print("record data :",record)
        not_found_id={"Status": "False", "Message": "No record found with the given ID"}
        if not record:
            return jsonify(not_found_id), 404
            
        cur.execute('UPDATE photobooth SET image=%s WHERE id=%s',(newfilename,record_id))
        conn.commit()
        
        success={"Status": "True", "Message": "Filename updated successfully"}
        failed={"Status": "False", "Message": "Unable to insert data at this moment"}
        if cur.rowcount > 0:
            conn.close()
            return jsonify(success,newfilename), 200
        
    except :
        return jsonify(failed), 500
    
if __name__=="__main__":
    app.run(port=5001,debug=True)
    