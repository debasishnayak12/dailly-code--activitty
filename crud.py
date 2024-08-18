from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)


def db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="api_test"
    )
    return conn

def validate_data(ballcoordinates):
    # Check if 'Ball_id', 'x', and 'y' are present and not empty
    if 'Ball_id' not in ballcoordinates or not isinstance(ballcoordinates['Ball_id'], int):
        return "Enter a valid integer for Ball_id"
    if 'x' not in ballcoordinates or not isinstance(ballcoordinates['x'], float):
        return "Enter a valid float for x Coordinates"
    if 'y' not in ballcoordinates or not isinstance(ballcoordinates['y'], float):
        return "Enter a valid float for y Coordinates"
    return None

@app.route('/')
def Home():
    return ("Api home page")

@app.route('/api/create/ballcoordinates', methods=["POST"])
def add_data():
    new_data = request.get_json()
    validation_error = validate_data(new_data)
    
    if validation_error:
        return jsonify({"Error": validation_error}), 400
    
    Ball_id = new_data.get('Ball_id')
    x = new_data.get('x')
    y = new_data.get('y')
    
    try:
        conn = db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO ballcoordinates (Ball_id, x, y) VALUES (%s, %s, %s)", (Ball_id, x, y))
        conn.commit()
        conn.close()
        return jsonify({"Status": "True", "Message": "Data inserted successfully"}), 201
    except :
        return jsonify({"Status": "False", "Message": "Unable to insert data at this moment"}), 500
    finally:
        if conn:
            conn.close()
    


# this is for read data
@app.route('/api/read_all/ballcoordinates',methods=["GET"])
def read_all():
    try:
        conn=db_connection()
        cur=conn.cursor(dictionary=True)
        cur.execute("select * from ballcoordinates ")
        result=cur.fetchall()
        conn.close()
        return jsonify(result),200
    except:
        return({"Error":"Database error","message":"Unable to fetch data "})

    
#THis is for read one data 
@app.route('/api/read_one/ballcoordinates/<int:Ball_id>', methods=["GET"]) # in this api int:ball_id will placed by ball_id
def get_one_data(Ball_id):
    try:
        conn = db_connection()
        cur = conn.cursor(dictionary=True)  # Fetch data as a dictionary
        cur.execute("SELECT * FROM ballcoordinates WHERE Ball_id = %s", (Ball_id,))
        result = cur.fetchone()  # Fetch a single record
        conn.close()
        
        if result is None:
            return jsonify({"Status":"False","Message":"Unabale to fetch data "}), 400
        return jsonify({"Status":"True","Message":"Successfully fetched data "},{result}),200
    except mysql.connector.Error as err:
        return jsonify({"Error": f"Database error: {err}"}), 500
    

#This is for update data PUT method
@app.route('/api/update_all/ballcoordinates/<int:Ball_id>',methods=["PUT"])
def update_data(Ball_id):
    new_data=request.get_json()
    x=new_data.get('x')
    y=new_data.get('y')

    try:
        conn=db_connection()
        cur=conn.cursor()
        update_query="update ballcoordinates set x=%s,y=%s where Ball_id=%s"
        cur.execute(update_query,(x,y,Ball_id))
        
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
@app.route("/api/update_any/ballcoordinates/<int:Ball_id>",methods=["PATCH"])
def update_any(Ball_id):
    new_data=request.get_json()
    x=new_data.get('x')
    y=new_data.get('y')
    
    conn=db_connection()
    
    data_to_update=[]
    values=[]
    
    if x is not None :
        data_to_update.append('x=%s')
        values.append(x)
    
    if y is not None :
        data_to_update.append('y=%s')
        values.append(y)
    
    if not data_to_update:
        return jsonify({"Status":"False","Message":"Unable to update data "}),400
        
    try:
        update_query=f"UPDATE ballcoordinates SET {', '.join(data_to_update)} WHERE Ball_id = %s"
        values.append(Ball_id)
        
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
@app.route('/api/delete/ballcoordiantes/<int:Ball_id>',methods=["DELETE"])
def delete_data(Ball_id):
    
    try:
        #check the Ball_id
        conn=db_connection()
        cur=conn.cursor()
        cur.execute("select * from ballcoordinates where Ball_id=%s",(Ball_id,))
        if cur.fetchone() is None :
            return jsonify({"Status ":"False","message":"ball_id not found"}),404
        #Delete query execute 
        conn1=db_connection()
        cur1=conn1.cursor()    
        cur1.execute("DELETE FROM ballcoordinates where Ball_id=%s",(Ball_id,))
        conn1.commit()
        return jsonify({"Status":"True","Message":"Data deleted successfully"}),200
    except mysql.connector.Error as err:
        return jsonify({"Error":f"Database error :{err}"})
    finally:
        if conn:
            conn.close()
if __name__ == "__main__":
    app.run(debug=True)
