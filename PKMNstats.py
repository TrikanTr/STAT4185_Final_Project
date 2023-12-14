from email.iterators import typed_subpart_iterator
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import sqlite3

from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.model_selection import train_test_split, GridSearchCV
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score


#import sqlite table into pandas dataframe
con = sqlite3.connect("pokemon.db")
df = pd.read_sql_query("SELECT * from poke_info", con)

print(df)

con.close()

#adding missing data from the website to the dataframe
df.loc[195] = ["Walking_Wake", "36426 Teams", "Water", "Dragon", 590, 99, 83, 91, 125, 83, 109, "Choice_Specs"]
df.loc[196] = ["Zamazenta", "30498 Teams", "Fighting", "None", 660, 92, 120, 115, 80, 115, 138, "Leftovers"]
df.loc[197] = ["Iron_Leaves", "1574 Teams","Grass", "Psychic", 590, 90, 130, 88, 70, 108, 104, "Choice_Band"]

#make usage column into percentage based data
df['usage'] = df['usage'].str.replace('\D', '', regex=True)
df['usage'] = pd.to_numeric(df['usage'])
df['usage'] = df['usage']/df['usage'].sum() * 100

#new column for boolean for if a pokemon has a usage on teams over 0.5%
df["usage_gt_0.2"] = df["usage"] > 0.2

X_lin = df["BST"]
Y_lin = df["usage"]
plt.scatter(X_lin, Y_lin)
plt.show()
#must close plot to continue program

#all numeric columns for using in ML models
columns_to_scale = ['BST','HP','ATK', 'DEF', 'SPA', 'SPD','SPE']
X = df[columns_to_scale]
y_use_raw = df["usage"] #for regression modeling
y = df["usage_gt_0.2"] #for random froest modeling
columns_no_scale = [col for col in X.columns if col not in columns_to_scale]

#random forest modeling
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, shuffle=True, stratify=y)
preprocessor = ColumnTransformer(
    transformers=[
        ('scaler', StandardScaler(), columns_to_scale)
    ]
)
X_train = preprocessor.fit_transform(X_train)
X_test = preprocessor.transform(X_test)

X_train = pd.DataFrame(X_train, columns=columns_to_scale)
X_test = pd.DataFrame(X_test, columns=columns_to_scale)

rf_classifier = RandomForestClassifier()
rf_classifier.fit(X_train, y_train)

y_pred = rf_classifier.predict(X_test)

#check accuracy stats
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='binary')
recall = recall_score(y_test, y_pred, average='binary')
f1 = f1_score(y_test, y_pred, average='binary')

print(f'Accuracy: {accuracy:.2f}')
print(f'Precision: {precision:.2f}')
print(f'Recall: {recall:.2f}')
print(f'F1 Score: {f1:.2f}')


#multiple linear regression model
X_usage_train, X_usage_test, y_usage_train, y_usage_test = train_test_split(X, y_use_raw, test_size=0.25, random_state=42, shuffle=True)
regr = LinearRegression()
regr.fit(X_usage_train, y_usage_train)
print(regr.coef_)

predict_usage = regr.predict(X_usage_test)

#calculate r^2 of the model
r2_score(y_usage_test, predict_usage)

#send final modified df to csv
df.to_csv('poke_info_final.csv', index=False)