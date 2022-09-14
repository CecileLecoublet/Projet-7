# 1. Library imports
import uvicorn
from fastapi import FastAPI
from BankNotes import BankNote
import pickle
import pandas as pd

# 2. Create the app object
app = FastAPI()
pickle_in = open("model copy.pkl","rb")
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
def predict_banknote(data:BankNote):
    data = data.dict()
    SK_ID_CURR = data['SK_ID_CURR']
   # print(classifier.predict([[variance,skewness,curtosis,entropy]]))
    prediction = classifier.predict(df[df["SK_ID_CURR"]== SK_ID_CURR]).tolist()
    return {'prediction': prediction}

# 5. Run the API with uvicorn
#    Will run on http://127.0.0.1:8000
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000, debug=True)
