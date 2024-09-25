from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)


def db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="atthah"
    )
    return conn

def validate_data(user):
    # Check if 'name', 'email', and 'mobile' are present and not empty
    # if 'name' not in user or  isinstance(user['name'], int) or  user['name']=="":
    if 'name' not in user or  user['name'].isdigit() or  user['name']=="":
        return "Enter a valid Name"
    if 'email' not in user or  "@" not in str(user['email']) or "." not in str(user["email"]) or user.get('email')=="":
        return "Enter a valid email"
    if 'mobile' not in user or not user['mobile'].isdigit() or not len(str(user["mobile"]))==10 or user.get('mobile')=="":
        return "Enter a valid Mobile number"
    return None

@app.route('/')
def Home():
    return ("Api home page")

@app.route('/user/create', methods=["POST"])
def add_data():
    new_data = request.form
    validation_error = validate_data(new_data)
    
    if validation_error:
        return jsonify({"Error": validation_error}), 400
    
    name = new_data.get('name')
    email = new_data.get('email')
    mobile = new_data.get('mobile')
    print("name :",name)
    print("email :",email)
    print("mobile :",mobile)
    
    try:
        conn = db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO user (name, email, mobile ) VALUES (%s, %s, %s)", (name, email, mobile))
        conn.commit()
        conn.close()
        return jsonify({"Status": "True", "Message": "Data inserted successfully"}), 201
    except :
        return jsonify({"Status": "False", "Message": "Unable to insert data at this moment"}), 500
    finally:
        if conn:
            conn.close()
    


# this is for read data
@app.route('/user/read_all',methods=["POST"])
def read_all():
    try:
        conn=db_connection()
        cur=conn.cursor(dictionary=True)
        cur.execute("select name,email,mobile,time  from user ")
        result=cur.fetchall()
        conn.close()
        return jsonify(result),200
    except:
        return({"Error":"Database error","message":"Unable to fetch data "})


#THis is for read one data 
@app.route('/user/read_one', methods=["POST"]) # in this api int:user_id will placed by actual user_id
def get_one_data():
    user_id=request.form.get('id')
    print("user id :",user_id)
    try:
        conn = db_connection()
        cur = conn.cursor(dictionary=True)  # Fetch data as a dictionary
        cur.execute("SELECT * FROM user WHERE id = %s", (user_id,))
        result = cur.fetchone()  # Fetch a single record
        conn.close()
        print(result)
        
        if result is None:
            return jsonify({"Status":"False","Message":"Unabale to fetch data "}), 400
        return jsonify({"Status":"True","Message":"Successfully fetched data "},f"{result}"),200
    except mysql.connector.Error as err:
        return jsonify({"Error": f"Database error: {err}"}), 500
    

#This is for update data PUT method
@app.route('/user/update_all',methods=["POST"])
def update_data():
    user_id=request.form.get('id')
    new_data=request.form
    
    validation_error = validate_data(new_data)
    
    if validation_error:
        return jsonify({"Error": validation_error}), 400
    
    name=new_data.get('name')
    email=new_data.get('email')
    mobile = new_data.get('mobile')

    try:
        conn=db_connection()
        cur=conn.cursor()
        update_query="update user set name=%s,email=%s,mobile=%s where id=%s"
        cur.execute(update_query,(name,email,mobile,user_id))
        
        conn.commit()
        
        if cur.rowcount == 0:
            return jsonify({"status":"False","message":"No changes occured at this moment"}),400
        return jsonify({"status":"True","message":"Data updated successfully"}),200
    
    except mysql.connector.Error as err:
        return jsonify({"Error":f"Database Error :{err}"}),500
    finally:
        if conn:
            conn.close()
            
#this is for update PATCH method
@app.route("/user/update_any",methods=["POST"])
def update_any():
    user_id=request.get('id')
    new_data=request.form
    
    name=new_data.get('name')
    email=new_data.get('email')
    mobile = new_data.get('mobile')
    
    conn=db_connection()
    
    data_to_update=[]
    values=[]
    
    if name is not None or not name== " ":
        data_to_update.append('name=%s')
        values.append(name)
        
    
    
    if email is not None :
           if "@" not in str(email) or "." not in str(email):
               return "Enter a valid email"
           else:
               data_to_update.append('email=%s')
               values.append(email)
 
    
    if mobile is not None :
        if not len(mobile)==10 or not mobile.isdigit():
            return "Enter a valid Mobile"
        else:
            data_to_update.append('mobile=%s')
            values.append(mobile)
 
    
    if not data_to_update:
        return jsonify({"Status":"False","Message":"Unable to update data "}),400
        
    try:
        update_query=f"UPDATE user SET {', '.join(data_to_update)} WHERE id = %s"
        values.append(user_id)
        
        cur=conn.cursor()
        cur.execute(update_query,tuple(values))
        conn.commit()
        
        return jsonify({"status":"True","Message":"Data updated successfuly"}),200
       
    
    except mysql.connector.Error as err:
        return jsonify({"Error":f"Database error :{err}"}),500
    
    finally:
        if conn:
            conn.close()
        
#This is for Delete data from table 
@app.route('/user/delete',methods=["DELETE"])
def delete_data():
    user_id=request.form.get('id')
    
    try:
        #check the Ball_id
        conn=db_connection()
        cur=conn.cursor()
        cur.execute("select * from user where id=%s",(user_id,))
        if cur.fetchone() is None :
            return jsonify({"Status ":"False","message":"user_id not found"}),404
        #Delete query execute 
        conn1=db_connection()
        cur1=conn1.cursor()    
        cur1.execute("DELETE FROM user where id=%s",(user_id,))
        conn1.commit()
        return jsonify({"Status":"True","Message":"Data deleted successfully"}),200
    except mysql.connector.Error as err:
        return jsonify({"Error":f"Database error :{err}"})
    finally:
        if conn:
            conn.close()
if __name__ == "__main__":
    app.run(debug=True)
