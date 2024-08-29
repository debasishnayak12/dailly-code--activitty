from flask import Flask,request
import mysql.connector
app=Flask(__name__)

def db_connect():
    conn=mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="webscraper"
    )
    return conn

@app.route('/get_data',methods=["GET"])
def get_data():
    try:
        conn=db_connect()
        cur=conn.cursor()
        cur.execute("SELECT contacts,captions,image_link from whatsapp")
        data=cur.fetchall()
        
        return data
    except Exception as e:
        print(f"Error occured in data collect {e}")
        
if __name__=="__main__":
    app.run(debug=True)