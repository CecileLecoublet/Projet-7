import requests
import streamlit as st
import pandas as pd
import json
from fastapi.encoders import jsonable_encoder
import plotly.express as px
from lightgbm import LGBMClassifier
import shap
shap.initjs()

tab = pd.read_csv("X_test_val.csv")

# Titre du document
st.title('Dashboard : Prédiction de crédit')

# Ouverture des fichiers
read_and_cache_csv = st.cache(pd.read_csv)

url = "http://127.0.0.1:8000/predict"

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

# Fonction qui fait un lien avec le FASTAPI
def main(val, df):

    df = df.iloc[val]

    df1 = df[["AMT_CREDIT", "AMT_ANNUITY", "AMT_GOODS_PRICE", "REGION_POPULATION_RELATIVE", "DAYS_BIRTH", 
                "DAYS_ID_PUBLISH", "OCCUPATION_TYPE", "WEEKDAY_APPR_PROCESS_START", "HOUR_APPR_PROCESS_START",
                "EXT_SOURCE_1", "EXT_SOURCE_2", "EXT_SOURCE_3", "AMT_REQ_CREDIT_BUREAU_YEAR"]]

    df_json = df1.to_json(orient='records')
    payload = df_json.strip("[]")

    headers = {
        'Content-Type' : 'application/json'
    }
    response = requests.post(url, headers = headers, data=payload)
    if response.json() == 0 :
        rep = 0
        st.success("Le client n'est pas à risque")
    else :
        rep = 1
        st.error("Le client est à risque")
    return rep

def fc_global(rep) :
    prov = pd.read_csv("X_train.csv")
    X_test = pd.read_csv("X_test.csv")
    col = prov.loc[ : , prov.columns != 'TARGET'].columns
    X = prov[col]
    y = prov["TARGET"]
    lgbc = LGBMClassifier(**{'n_estimators': 250, 'objective': 'binary', 'class_weight':'balanced', 'random_state':100})
    lgbc.fit(X, y)
    y_pred = lgbc.predict(X_test)
    # get importance
    importance = lgbc.feature_importances_
    # plot feature importance
    fig = px.bar([x for x in range(len(importance))], x= X.columns, y = importance)
    st.plotly_chart(fig, use_container_width=True)
    explainer = shap.TreeExplainer(lgbc)
    shap_values = explainer.shap_values(X_test)
    if rep == 0 :
        st.set_option('deprecation.showPyplotGlobalUse', False)
        fig_1 = shap.summary_plot(shap_values[0], X_test, plot_type="bar")
    else :
        st.set_option('deprecation.showPyplotGlobalUse', False)
        fig_1 = shap.summary_plot(shap_values[1], X_test, plot_type="bar")
    st.pyplot(fig_1)

if __name__ == '__main__':
    df = read_and_cache_csv("X_test.csv")

    st.markdown("## Premier chapitre : Statut du crédit client")
    choix = st.selectbox("Choix du client", tab["SK_ID_CURR"])
    data = tab[tab["SK_ID_CURR"] == choix]
    val = tab[tab["SK_ID_CURR"] == choix].index
    rep = main(val, df)

    st.markdown("## Deuxième chapitre : Statut du client")
    age = data['DAYS_BIRTH'].round(0)
    st.write("L'âge du client est : ", age)
    statut = ['Laborers', 'Core staff', 'Accountants', 'Managers', 'Drivers', 'Sales staff', 'Cleaning staff', 'Cooking staff',
            'Private service staff', 'Medicine staff', 'Security staff', 'High skill tech staff', 'Waiters/barmen staff',
            'Low-skill Laborers', 'Realty agents', 'Secretaries', 'IT staff', 'HR staff']
    for i in range(0, len(statut), 1):
        if data["OCCUPATION_TYPE"].values == i:
            st.write("Le client travaille dans :", statut[i])

    st.markdown("## Troisième chapitre : Information sur le crédit")
    graphique(data)
    quatrieme_chapitre(data, val)
    st.markdown("## Cinquième chapitre : Features gloabl et features local")
    fc_global(rep)