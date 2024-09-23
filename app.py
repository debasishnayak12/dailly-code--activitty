from flask import Flask,render_template,request,jsonify
import mysql.connector


app =Flask(__name__)

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
    
@app.route('/postdata',methods=["POST"])
def postdata():
    if request.method =="POST":
        data = request.json
        name = data.get('name')
        phone = data.get('phone')
        print(name,phone)
        if not name or not phone  :
            return jsonify({"Error":"anme and phone data required"})
        try:
            conn = db_connection()
            cur = conn.cursor(dictionary=True)
            query = "insert into customers(Name,Phone) values(%s,%s)"
            val = (name,phone)
            cur.execute(query,val)
            conn.commit()
            return jsonify({"Status":"True","message":"Insert data"})

        except mysql.connector.Error as e:
            return jsonify({"Status":"False","Message":f"{e}"})
        # with open(f"{request.form.get('name')}.txt" ,"w") as f:
        #     f.write("POST created ")
        

        
if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)