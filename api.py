from flask import Flask,request,jsonify
import mysql.connector

app = Flask(__name__)

def db_conn():
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        passwd = "",
        db = "api_test"
    )
    return mydb

# def validate(phone):
#     if len(phone)!=10 or not isinstance(phone,str):

#         return "Enter valid 10digit number"
#     return None

@app.route('/insert-data',methods = ["POST"])
def insert_data():
    name = request.form.get('name')
    phone = request.form.get('phone')
    
    # validation_error = validate(phone)
    # if validation_error:
    #     return jsonify({"Error":validation_error}),400
    
    try:
        conn = db_conn()
        cur = conn.cursor()
        cur.execute("INSERT INTO customers(Name,Phone) VALUES(%s,%s)",(name,phone))
        conn.commit()
        conn.close()
        
        return jsonify({"Status ":"True","Message":"Data inserted succesfully"}),201
    except mysql.connector.Error as e:
        return jsonify({"Status":"False","Message":f"{e}"}),500
        
    
    
    
if __name__=="__main__":
    app.run(debug=True)