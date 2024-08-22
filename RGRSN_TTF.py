import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn import preprocessing

df = pd.read_excel("Opto-Mechanical_Failure Records_and_Inventory.xlsx")
enc = preprocessing.OrdinalEncoder()
X = df[["Hutch", "Serial Number W/O Production Number", "PV Base"]]

enc.fit(X)
X = enc.transform(X)
Y = df["Time to Failure"]


X_train,X_test,Y_train,Y_test = train_test_split(X, Y, test_size = 0.2, random_state=1)


theLinReg = LinearRegression()
theLinReg.fit(X_train,Y_train)
thePredicitions = theLinReg.predict(X_test)
print(thePredicitions)
