import requests

def send_data(Name,email,Mobile):
    
    url="http://127.0.0.1:5000/add_details"
    
    data={
        "Name":Name,
        "email":email,
        "Mobile":Mobile
    }
    
    response=requests.post(url,data=data)
    if response.status_code==201:
        result=response.json()
        print("Data inserted successfully!")
        print("id",result['id'])
        
        return response
    