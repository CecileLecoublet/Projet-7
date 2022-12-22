import requests
import streamlit as st
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import lime
from lime import lime_tabular
import pickle
st.set_option('deprecation.showPyplotGlobalUse', False)
showPyplotGlobalUse = False

tab = pd.read_csv("../../data/X_test.csv")

def load_model():
    pickle_in = open("../mlflow_model/model.pkl","rb")
    clf = pickle.load(pickle_in)
    return clf

# Titre du document
st.title('Dashboard : Prédiction de crédit')

# Ouverture des fichiers
read_and_cache_csv = st.cache(pd.read_csv)

url = f"http://127.0.0.1:8000/predict"

def graphique(data):
    prov = data[["AMT_INCOME_TOTAL", "AMT_CREDIT", "AMT_ANNUITY", "AMT_GOODS_PRICE"]].copy()

    prov.rename(columns={'AMT_INCOME_TOTAL': 'Salaire', 'AMT_CREDIT': 'Crédit',
                        'AMT_ANNUITY': 'Rente', "AMT_GOODS_PRICE": "Prix des biens"}, inplace=True)

    bar_chart = px.bar(prov, barmode='group', text_auto='.2s').update_xaxes(categoryorder = "total descending")
    st.write(bar_chart)

def quatrieme_chapitre(data, val):

    st.markdown("## Quatrième chapitre : Note Appartement / Ville / Régions")

    st.markdown("Dans ce chapitre, les notes des clients sur leur appartement, ville et régions seront consignées. Note interne et externe.\
        Une note élevée montre une ville avec beaucoup de population, une ville active.")

    st.write("Score normalisé à partir d'une source de données externe")

    prov = data[["EXT_SOURCE_1", "EXT_SOURCE_2", "EXT_SOURCE_3"]].copy()
    bar_chart = px.bar(prov, barmode='group').update_xaxes(categoryorder = "total descending")
    bar_chart.update_layout(yaxis=dict(range=[0,1]))
    st.write(bar_chart)


def fc_global(X_test_scaled) :

    explainer = lime_tabular.LimeTabularExplainer(
        training_data=np.array(X_train_scaled),
        feature_names=X_train_scaled.columns,
        class_names=['Positif', 'Negatif'],
        mode='classification')

    index = X_test_scaled[X_test_scaled["SK_ID_CURR"] == choix].index
    exp = explainer.explain_instance(
        data_row = X_test_scaled.iloc[index[0]], 
        predict_fn = load_model().predict_proba)

    exp.as_pyplot_figure()
    st.pyplot()
    plt.clf()
    exp.show_in_notebook(show_table=True)


# Fonction qui fait un lien avec le FASTAPI
def main(df):

    client = df["SK_ID_CURR"]

    df_json = client.to_json(orient='records')
    payload = df_json.strip("[]")

    headers = {
        'Content-Type' : 'application/json'
    }
    url = "http://127.0.0.1:8000/predict?data="+payload

    response = requests.post(url)

    if response.json() == 0 :
        rep = 0
        st.success("Le client n'est pas à risque")
    else :
        rep = 1
        st.error("Le client est à risque")
    return rep

if __name__ == '__main__':
    df = read_and_cache_csv("../../data/X_test_scaled.csv")
    X_train_scaled = read_and_cache_csv("../../data/X_train_scaled.csv")

    st.markdown("## Premier chapitre : Statut du crédit client")
    choix = st.selectbox("Choix du client", df["SK_ID_CURR"])
    data = df[df["SK_ID_CURR"] == choix]
    tab_1 = tab[tab["SK_ID_CURR"] == choix]
    rep = main(data)

    st.markdown("## Deuxième chapitre : Statut du client")
    age = tab_1['DAYS_BIRTH'].round(0)
    st.write("L'âge du client est : ", age.values[0])
    statut = ['Laborers', 'Core staff', 'Accountants', 'Managers', 'Drivers', 'Sales staff', 'Cleaning staff', 'Cooking staff',
            'Private service staff', 'Medicine staff', 'Security staff', 'High skill tech staff', 'Waiters/barmen staff',
            'Low-skill Laborers', 'Realty agents', 'Secretaries', 'IT staff', 'HR staff']
    for i in range(0, len(statut), 1):
        if tab_1["OCCUPATION_TYPE"].values == i:
            st.write("Le client travaille dans :", statut[i])

    st.markdown("## Troisième chapitre : Information sur le crédit")
    graphique(tab_1)
    quatrieme_chapitre(tab_1, choix)
    st.markdown("## Cinquième chapitre : Features global et features local")
    fc_global(df)