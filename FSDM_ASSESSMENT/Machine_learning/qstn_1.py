import pandas pd 
import numpy as np

from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

data=pd.read_csv(r"https://raw.githubusercontent.com/debasishnayak12/DATASETS/main/instagram_reach.csv")

model=MultiOutputRegressor(RandomForestRegressor())

X=data.iloc[:,:-2]
y=data.iloc[:,-2:]
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=40)

for i in data.columns:
    if X_train[i].dtypes=="O":
        X_train[i]=L.fit_transform(X_train[i])
    elif X_test[i].dtypes=="O":
        X_test[i]=L.transform(X_test[i])
        
    else:
        pass
    
model.fit(X_train,y_train)
pred=model.predict(X_test)
print(f"The predicted answer is {pred}")
        