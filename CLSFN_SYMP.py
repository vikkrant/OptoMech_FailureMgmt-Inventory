from pandas import read_excel
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn import preprocessing

dF = read_excel("Opto-Mechanical_Failure Records_and_Inventory.xlsx")
enc = preprocessing.OrdinalEncoder()
le = preprocessing.LabelEncoder()
mlb = preprocessing.MultiLabelBinarizer()
X = dF[["Hutch", "Serial Number W/O Production Number", "PV Base"]]
Y = dF["Standardized"]

X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size = 0.2, random_state=1)

clf = GaussianNB()
clf.fit(X_train,Y_train)

outProb = clf.predict_proba(X_test)
