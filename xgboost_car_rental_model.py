# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 15:26:30 2018

@author: Nabeel
"""

import pandas as pd
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder
import numpy as np
from sklearn.metrics import mean_squared_error

# Load the data
train_df = pd.read_csv('F:\\work_2\\social_dice\\practical_test\\cars_rental\\train.csv', header=0)
test_df = pd.read_csv('F:\\work_2\\social_dice\\practical_test\\cars_rental\\test.csv', header=0)

train_df.time=pd.to_datetime(train_df.time,infer_datetime_format=True)
test_df.time=pd.to_datetime(test_df.time,infer_datetime_format=True)
train_df['month']=train_df.time.dt.month
test_df['month']=test_df.time.dt.month
train_df['hour']=train_df.time.dt.hour
test_df['hour']=test_df.time.dt.hour

feature_columns_to_use =['hour','month', 'season', 'nonworkingday', 'workingday', 'weather', 'tmpdegree',
                         'atmpdegree', 'hum', 'windspeed']

train_df.columns=['time', 'season', 'nonworkingday', 'workingday', 'weather', 'tmpdegree',
       'atmpdegree', 'hum', 'windspeed', 'csl', 'reg', 'count', 'month', 'hour']

# Prepare the inputs for the model
train_X = train_df.loc[:,feature_columns_to_use].as_matrix()
train_y = train_df['count'].as_matrix()

from sklearn import model_selection
X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(train_X, train_y, test_size=0.3, random_state=1234)



# You can experiment with many other options here, using the same .fit() and .predict()
# methods; see http://scikit-learn.org
# This example uses the current build of XGBoost, from https://github.com/dmlc/xgboost
gbm = xgb.XGBClassifier(max_depth=3, n_estimators=50, learning_rate=0.05,nthread=4).fit(train_X, train_y)

predictions = gbm.predict(X_validation)
mse=mean_squared_error(Y_validation,predictions)
import math
rmse=math.sqrt(mse)
print("xgboost rmse:",rmse)

#random forest to compare
from sklearn.ensemble import RandomForestRegressor
clf = RandomForestRegressor(max_depth=2, random_state=0)
clf.fit(X_train, Y_train)
pred_randomforest=clf.predict(X_validation)
mse_rf=mean_squared_error(Y_validation,pred_randomforest)
rmse_rf=math.sqrt(mse_rf)
print("random forest",rmse_rf)