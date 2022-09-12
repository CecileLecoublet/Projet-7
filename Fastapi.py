# 1. Library imports
import uvicorn
from fastapi import FastAPI
from BankNotes import BankNote
import numpy as np
import pickle
import pandas as pd
# 2. Create the app object
app = FastAPI()
pickle_in = open("model copy.pkl","rb")
classifier=pickle.load(pickle_in)

import streamlit as st
import pandas as pd
# Ouverture des fichiers
read_and_cache_csv = st.cache(pd.read_csv)
df = read_and_cache_csv("X_test.csv")

# 3. Index route, opens automatically on http://127.0.0.1:8000
@app.get('/')
def index():
    return {'message': 'Hello, World'}

# 3. Expose the prediction functionality, make a prediction from the passed
#    JSON data and return the predicted Bank Note with the confidence
@app.post('/predict')
def predict_banknote(data:BankNote):
    data = data.dict()
    AMT_CREDIT = data['AMT_CREDIT']
    AMT_ANNUITY = data['AMT_ANNUITY']
    AMT_GOODS_PRICE = data['AMT_GOODS_PRICE']
    REGION_POPULATION_RELATIVE =data['REGION_POPULATION_RELATIVE']
    DAYS_BIRTH = data['DAYS_BIRTH']
    DAYS_ID_PUBLISH = data['DAYS_ID_PUBLISH']
    OCCUPATION_TYPE = data['OCCUPATION_TYPE']
    WEEKDAY_APPR_PROCESS_START = data['WEEKDAY_APPR_PROCESS_START']
    HOUR_APPR_PROCESS_START = data['HOUR_APPR_PROCESS_START']
    EXT_SOURCE_1 = data['EXT_SOURCE_1']
    EXT_SOURCE_2 = data['EXT_SOURCE_2']
    EXT_SOURCE_3 = data['EXT_SOURCE_3']
    AMT_REQ_CREDIT_BUREAU_YEAR = data['AMT_REQ_CREDIT_BUREAU_YEAR']
   # print(classifier.predict([[variance,skewness,curtosis,entropy]]))
    prediction = classifier.predict(df).tolist()[0]
    return prediction

# 5. Run the API with uvicorn
#    Will run on http://127.0.0.1:8000
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)