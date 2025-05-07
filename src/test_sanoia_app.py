
#Installation des dépendances
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

#Titre de l'application

st.title("Analyse des données de la base Open Medic")

#Téléchargement des fichiers

uploaded_file_2024 = st.file_uploader("Importer le premier fichier NB_2024.csv", type="csv")
uploaded_file_2023 = st.file_uploader("Importer le deuxième fichier NB_2023.csv", type="csv")
uploaded_file_2022 = st.file_uploader("Importer le troisième fichier NB_2022.csv", type="csv")

#Création d'une base SQLite en mémoire
base_total = sqlite3.connect(":memory:")

#Lecture des fichier et chargement dans la base SQLite

if uploaded_file_2024 is not None:
    fichier_2024 = pd.read_csv(uploaded_file_2024, sep=';', encoding='latin-1')
    fichier_2024['Annee'] = 2024
    fichier_2024.to_sql("fichier_total", base_total, if_exists="replace", index=False)

if uploaded_file_2023 is not None:
    fichier_2023 = pd.read_csv(uploaded_file_2023, sep=';', encoding='latin-1')
    fichier_2023['Annee'] = 2023
    fichier_2023.to_sql("fichier_total", base_total, if_exists="append", index=False)

if uploaded_file_2022 is not None:
    fichier_2022 = pd.read_csv(uploaded_file_2022, sep=';', encoding='latin-1')
    fichier_2022['Annee'] = 2022
    fichier_2022.to_sql("fichier_total", base_total, if_exists="append", index=False)



#Queries

if uploaded_file_2024 or uploaded_file_2023 or uploaded_file_2022:

    #Query_1: Nombre de HUMIRA consommé en total

    Query_1 = """
    SELECT Annee, SUM(nbc) as Nb_consommants
    FROM fichier_total
    WHERE l_cip13 like ?
    group by Annee
    ORDER BY Annee desc
    """
    resultat_1 = pd.read_sql_query(Query_1, base_total, params=['HUMIRA%'])
    st.subheader("Nombre total de HUMIRA consommé")
    st.write(resultat_1)

    if uploaded_file_2024 and uploaded_file_2023 and uploaded_file_2022:

        #Graphique 1
        st.subheader("Graphique - Nombre de HUMIRA consommé en total")
        fig, ax = plt.subplots()
        resultat_1.plot(x='Annee', y='Nb_consommants', kind='bar', ax=ax)
        ax.set_title=('Nombre de HUMIRA consommé en total')
        st.pyplot(fig)
    else:
        pass

    #Query_2: Nombre de HUMIRA consommé par dispositif d'injection
    Query_2 = """
    SELECT Annee,
        SUM(CASE WHEN l_cip13 LIKE 'HUMIRA%SER%' THEN nbc ELSE 0 END) as Nb_Humira_par_seringue,
        SUM(CASE WHEN l_cip13 LIKE 'HUMIRA%STYLO%' THEN nbc ELSE 0 END) as Nb_Humira_par_stylo
    FROM fichier_total
    WHERE l_cip13 LIKE 'HUMIRA%'
    group by Annee
    ORDER BY Annee desc
    """
    resultat_2 = pd.read_sql_query(Query_2, base_total)
    st.subheader("Nombre de HUMIRA consommé par dispositif d'injection")
    st.write(resultat_2)

    if uploaded_file_2024 and uploaded_file_2023 and uploaded_file_2022:

        #Graphique 2
        st.subheader("Graphique - Nombre de HUMIRA consommé par dispositif d'injection")
        fig, ax = plt.subplots()
        resultat_2.plot(x='Annee', y=['Nb_Humira_par_seringue', 'Nb_Humira_par_stylo'], kind='bar', ax=ax)
        ax.set_title=('Nombre de HUMIRA consommé par dispositif d\'injection')
        st.pyplot(fig)
    else:
        pass

    #Query_3: Nombre de HUMIRA consommé par tranche d'age
    Query_3 = """
    SELECT Annee, age as Age, SUM(nbc) as Nb_consommants
    FROM fichier_total
    WHERE l_cip13 like ?
    group by Annee, age
    ORDER BY Annee desc, age asc
    """
    resultat_3 = pd.read_sql_query(Query_3, base_total, params=['HUMIRA%'])
    resultat_3_pivot = resultat_3.pivot(index='Age', columns='Annee', values='Nb_consommants')
    st.subheader("Nombre de HUMIRA consommé par tranche d'age")
    st.write(resultat_3_pivot)

    if uploaded_file_2024 and uploaded_file_2023 and uploaded_file_2022:

        #Graphique 3
        st.subheader("Graphique - Nombre de HUMIRA consommé par tranche d'age")
        fig, ax = plt.subplots()
        resultat_3_pivot.T.plot(kind='bar', ax=ax)
        ax.set_title=('Nombre de HUMIRA consommé par tranche d\'age')
        st.pyplot(fig)
    else:
        pass

    #Query_4: Nombre de HUMIRA consommé par région
    Query_4 = """
    SELECT Annee, BEN_REG as Region, SUM(nbc) as Nb_consommants
    FROM fichier_total
    WHERE l_cip13 like ?
    group by Annee, BEN_REG
    ORDER BY Annee desc, BEN_REG asc
    """
    resultat_4 = pd.read_sql_query(Query_4, base_total, params=['HUMIRA%'])

    resultat_4_pivot = resultat_4.pivot(index='Region', columns='Annee', values='Nb_consommants')
    st.subheader("Nombre de HUMIRA consommé par région")
    st.write(resultat_4_pivot)

    #Query_5: Nombre de HUMIRA consommé par prescripteur
    Query_5 = """
    SELECT Annee, PSP_SPE as Prescripteur, SUM(nbc) as Nb_consommants
    FROM fichier_total
    WHERE l_cip13 like ?
    group by Annee, PSP_SPE
    ORDER BY Annee desc, PSP_SPE asc
    """
    resultat_5 = pd.read_sql_query(Query_5, base_total, params=['HUMIRA%'])
    resultat_5_pivot = resultat_5.pivot(index='Prescripteur', columns='Annee', values='Nb_consommants')
    st.subheader("Nombre de HUMIRA consommé par prescripteur")
    st.write(resultat_5_pivot)

    #Query_6: Nombre de HUMIRA consommé par dispositif d'injection, par tranche d'âge, par région, par prescripteur
    Query_6 = """
    SELECT Annee,
        age as Age,
        BEN_REG as Region,
        PSP_SPE as Prescripteur,
        SUM(CASE WHEN l_cip13 LIKE 'HUMIRA%SER%' THEN nbc ELSE 0 END) as Nb_Humira_par_seringue,
        SUM(CASE WHEN l_cip13 LIKE 'HUMIRA%STYLO%' THEN nbc ELSE 0 END) as Nb_Humira_par_stylo
    FROM fichier_total
    WHERE l_cip13 like ?
    GROUP BY Annee, age, BEN_REG, PSP_SPE
    ORDER BY Annee desc, age asc, BEN_REG asc, PSP_SPE asc
    """
    resultat_6 = pd.read_sql_query(Query_6, base_total, params=['HUMIRA%'])
    resultat_6_pivot = resultat_6.pivot(index=['Age', 'Region', 'Prescripteur'], columns='Annee', values=['Nb_Humira_par_seringue', 'Nb_Humira_par_stylo'])
    st.subheader("Nombre de HUMIRA consommé par dispositif d'injection, par tranche d'âge, par région, par prescripteur")
    st.write(resultat_6_pivot)
else:
    st.warning("Veuillez importer au moins un fichier CSV")

