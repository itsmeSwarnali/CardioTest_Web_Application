import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, plot_roc_curve, classification_report, accuracy_score 
from sklearn.ensemble import RandomForestClassifier


df = pd.read_csv("E:\project01\cardio_train.csv\\Cardio.csv")

x = df.drop(["target"],axis=1)
y = df["target"]

xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size = .20, random_state = 42)

rf = RandomForestClassifier()
rf.fit(xtrain, ytrain)


accuracy = rf.score(xtest,ytest)

rf.predict(xtest)


#creating picle object
pickle.dump(rf, open('cardio.pkl','wb'))

rf = pickle.load(open('cardio.pkl','rb'))



