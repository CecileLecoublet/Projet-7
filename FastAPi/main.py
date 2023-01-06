# 1. Library imports
from fastapi import FastAPI
#from BankNotes import BankNote
import pickle
import uvicorn
import pandas as pd

# 2. Create the app object
app = FastAPI()
pickle_in = open("mlflow_model/model.pkl","rb")
classifier=pickle.load(pickle_in)

# Ouverture des fichiers
df = pd.read_csv("Dashboard/X_test_scaled.csv")

# 3. Index route, opens automatically on http://127.0.0.1:8000
@app.get('/')
def index():
    return {'message': 'Hello, World'}

# 4. Expose the prediction functionality, make a prediction from the passed
#    JSON data and return the predicted Bank Note with the confidence
@app.post('/predict')
async def predict_banknote(data:float):
    SK_ID_CURR = data
    prediction = classifier.predict(df[df["SK_ID_CURR"]== SK_ID_CURR]).tolist()[0]
    return prediction

# # 5. Run the API with uvicorn
# #    Will run on http://127.0.0.1:8000
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=443, debug=True, reload=True,  reload_dirs = ["html_files"],
                ssl_keyfile="./key.pem", 
                ssl_certfile="./cert.pem"
                )
