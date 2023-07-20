class Car:
    def __init__(self,brand,model):
        self.brand=brand
        self.model=model
        
    def display(self):
        print(f"my car is {self.brand} and the model is {self.model}")