import pandas 
from sklearn import preprocessing as pp
df = pandas.read_excel("724Ready.xlsx")
compRecords = {}
mlb = pp.MultiLabelBinarizer()


def multiLabelClassification():
    Y = list(df["Standardized"])
    for (k,v) in enumerate(Y):
        if "," in v:
            Y[k] = v.split(",")
        else:
            Y[k] = [v]

    return mlb.fit_transform(Y)




def classifyFailures():
    allComp = df["Classification"]
    failedComponents = []
    for (k,v) in enumerate(allComp):
        if v == "Failure":
            failedComponents.append(k)

    return failedComponents



def compModelsRatio():
    for index in range(0,df.shape[0]):
        dfElement = df.iloc[index]
        serNum = dfElement["Serial Number W/O Production Number"]
        
        if dfElement["Classification"] == "Failure":
            failedComponent = 1
        else:
            failedComponent = 0

        if serNum in compRecords:
            compRecords[serNum] = (compRecords[serNum][0] + failedComponent, compRecords[serNum][1] + 1)
        else:
            compRecords[serNum] = (failedComponent, 1)

    return compRecords