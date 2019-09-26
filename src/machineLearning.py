import pandas
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model

filepath = "../Data/jobs104_20190822_金融IT_parsed.xlsx"
df = pandas.read_excel(io=filepath)

def linearRegression(column1,column2):
    X = df[column1]
    Y = df[column2]
    X = X.values.reshape(-1,1)
    Y = Y.values.reshape(-1,1)
    X_train = X[:200]
    X_test = X[200:]

    Y_train = Y[:200]
    Y_test = Y[200:]

    plt.scatter(X_test, Y_test,  color='black')
    plt.title("LinearRegression of {} and {}".format(column1,column2))
    plt.xlabel(column1)
    plt.ylabel(column2)
    regr = linear_model.LinearRegression()
    regr.fit(X_train,Y_train)
    plt.plot(X_test, regr.predict(X_test),color='red',linewidth=3)
    plt.show()
print(df.info())
columns=['appliedNumber', 'required', 'salary', 'experience']

#'experience', 'appliedNumber'
#'experience', 'required'