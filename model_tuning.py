# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 10:20:41 2022

@author: 91993
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('eda_data.csv')

# choose relevant columns
df_model = df[['avg_salary','rating', 'size', 'type_of_ownership', 'industry', 'sector', 'revenue', 'company_age', 'python_yn', 'excel_yn', 'sql_yn', 'r_yn', 'job_simplified', 'seniority', 'desc_length']]

# get dummydata
df_dummy = pd.get_dummies(df_model)

# train test split
from sklearn.model_selection import train_test_split

X = df_dummy.drop('avg_salary', axis=1)

y = df_dummy.avg_salary.values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# multiple linear regression



# lasso regression
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Lasso, LinearRegression, Ridge
from sklearn.model_selection import cross_val_score, cross_validate
from sklearn.metrics import mean_squared_error


scalar = StandardScaler()
scalar.fit(X_train)
X_train = scalar.transform(X_train)
X_test = scalar.transform(X_test)
# X_eval = scalar.transform(X_eval)

model_lasso = Lasso()
model_lasso.fit(X_train, y_train)
scores = cross_val_score(model_lasso,X_train,y_train, scoring='neg_mean_squared_error', cv=5)
np.mean(scores)

alpha = []
errors = []
model_score = []

for i in range(1,100):
    alpha.append(i/100)
    model_lasso = Lasso(alpha=(i/10))
    model_lasso.fit(X_train, y_train)
    scores = cross_val_score(model_lasso,X_train,y_train, scoring='neg_mean_squared_error', cv=5)
    model_score.append(model_lasso.score(X_train, y_train))
    errors.append(abs(scores.mean()))
    
err = tuple(zip(alpha, errors, model_score))
df_err = pd.DataFrame(err,columns=['alpha', 'errors', 'model_score'])
# df_err[df_err.errors == min(df_err.errors)]
# lasso_cv_model_1 = LassoCV(eps=0.001,n_alphas=100,cv=5, max_iter=1000)
# lasso_cv_model_1.fit(X_train, y_train)



# Elastic net
from sklearn.linear_model import ElasticNetCV
elastic_model = ElasticNetCV(l1_ratio=[.1,.5,.7,.95,1], eps=0.0001, n_alphas=100, max_iter=10000000)

elastic_model.fit(X_train, y_train)   

y_pred = elastic_model.predict(X_test)
mean_squared_error(y_test,y_pred)


# linear regression
model_lm = LinearRegression()

scores = cross_validate(model_lm, X_train, y_train, scoring=['neg_mean_squared_error', 'neg_mean_absolute_error'], cv=5)
scores = pd.DataFrame(scores)

model_lm.fit(X_train, y_train)

y_final_test_pred = model_lm.predict(X_test)
mean_squared_error(y_test,y_final_test_pred)


# random forest
# tune this models using GridSearchCV
# test ensembles
