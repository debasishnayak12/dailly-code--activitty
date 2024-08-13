from src.HOUSEPRICEPRED.pipeline.prediction_pipeline import customdata,PredictPipeline
from flask import Flask,render_template,request

app=Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/predict',methods=["GET","POST"])
def get_predict():
     if request.method == "POST":
        data = customdata(
            area=float(request.form['area']),
            bedrooms=float(request.form['bedrooms']),
            bathrooms=float(request.form['bathrooms']),
            stories=float(request.form['stories']),
            mainroad=request.form['mainroad'],
            guestroom=request.form['guestroom'],
            basement=request.form['basement'],
            hotwaterheating=request.form['hotwaterheating'],
            airconditioning=request.form['airconditioning'],
            parking=float(request.form['parking']),
            prefarea=request.form['prefarea'],
            furnishingstatus=request.form['furnishingstatus']
        )
        
        final_data=data.get_data_as_dataframe()
        
        Predict_pipeline=PredictPipeline()
        
        pred=Predict_pipeline.predict(final_data)
        
        result=round(pred[0],2)
        
        return render_template("result.html",Final_result=result)
    
if __name__=="__main__":
    app.run(debug=True)