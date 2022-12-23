import streamlit as st
import plotly.express as px
st.set_option('deprecation.showPyplotGlobalUse', False)
showPyplotGlobalUse = False

# Note extérieure
# Quatrième chapitre
def quatrieme_chapitre(data, val):
    st.markdown("## Quatrième chapitre : Note Appartement / Ville / Régions")
    st.markdown("Dans ce chapitre, les notes des clients sur leur appartement,\
                ville et régions seront consignées. Note interne et externe.\
                 Une note élevée montre une ville avec beaucoup de population, une ville active.")
    st.write("Score normalisé à partir d'une source de données externe")
    #Affichage des graphiques
    prov = data[["EXT_SOURCE_1", "EXT_SOURCE_2", "EXT_SOURCE_3"]].copy()
    bar_chart = px.bar(prov, barmode='group').update_xaxes(categoryorder = "total descending")
    bar_chart.update_layout(yaxis=dict(range=[0,1]))
    st.write(bar_chart)