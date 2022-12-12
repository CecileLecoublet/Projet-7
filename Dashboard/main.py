# 1. Library imports
import uvicorn
from fastapi import FastAPI
from BankNotes import BankNote
import pickle
import pandas as pd
import shap

# 2. Create the app object
app = FastAPI()
pickle_in = open("model.pkl","rb")
classifier=pickle.load(pickle_in)

# Ouverture des fichiers
df = pd.read_csv("X_test.csv")

# 3. Index route, opens automatically on http://127.0.0.1:8000
@app.get('/')
def index():
    return {'message': 'Hello, World'}

# 3. Expose the prediction functionality, make a prediction from the passed
#    JSON data and return the predicted Bank Note with the confidence
@app.post('/predict')
async def predict_banknote(data:float):
    SK_ID_CURR = data
    prediction = classifier.predict(df[df["SK_ID_CURR"]== SK_ID_CURR]).tolist()[0]
    return prediction

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000, debug=True)
