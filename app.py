from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# @app.route('/save-measurement', methods=['POST'])
# def save_measurement():
#     data = request.get_json()
#     zoom_percentage = data.get('zoom_percentage')
#     distance_to_top = data.get('distance_to_top')
#     distance_to_right = data.get('distance_to_right')
    
#     # Save these values to your database
#     save_to_database(zoom_percentage, distance_to_top, distance_to_right)
    
#     return jsonify({"message": "Measurements saved successfully"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
