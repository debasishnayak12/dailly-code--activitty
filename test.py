from flask import Flask,render_template,request

app=Flask(__name__)

@app.route('/')

def home():
    return render_template("index.html")

@app.route('/final',methods=["GET","POST"])

def predict():
    if request.method == "POST":
        return render_template("Result.html")
    
if __name__=="__main__":
    app.run(debug=True,host="0.0.0.0")