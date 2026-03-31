import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Parkshare Dashboard", layout="wide")

# Lecture du fichier
DATA_PATH = Path(__file__).resolve().parent / "Sources_clean" / "kpi_potentiel_communes.csv"
df_score = pd.read_csv(DATA_PATH, low_memory=False)

# Colonnes derivees utiles pour les graphiques
df_score["taux_motorisation"] = (
    df_score["nb_vehicules"] / df_score["population_totale"].replace(0, pd.NA)
)
df_score["ratio_stationnement_logements"] = (
    df_score["total_lots_stationnement"] / df_score["nb_logements"].replace(0, pd.NA)
)

st.title("Dashboard d’analyse du potentiel commercial Parkshare")
st.markdown("Analyse des communes à fort potentiel pour la prospection commerciale.")

# =========================
# SIDEBAR - FILTRES
# =========================
st.sidebar.header("Filtres")

# Filtre département
deps = ["Tous"] + sorted(df_score["nom_dep"].dropna().unique().tolist())
dep_choisi = st.sidebar.selectbox("Département", deps)

# Dataset temporaire pour alimenter le filtre commune
df_temp = df_score.copy()
if dep_choisi != "Tous":
    df_temp = df_temp[df_temp["nom_dep"] == dep_choisi]

# Filtre commune
communes = ["Toutes"] + sorted(df_temp["nom_commune"].dropna().unique().tolist())
commune_choisie = st.sidebar.selectbox("Commune", communes)

# Filtre segment
priorites = ["Toutes"] + sorted(df_score["priorite"].dropna().unique().tolist())
priorite_choisie = st.sidebar.selectbox("Priorité", priorites)

# Filtre score
score_min, score_max = st.sidebar.slider(
    "Score potentiel",
    float(df_score["score_potentiel"].min()),
    float(df_score["score_potentiel"].max()),
    (
        float(df_score["score_potentiel"].min()),
        float(df_score["score_potentiel"].max())
    )
)

# =========================
# APPLICATION DES FILTRES
# =========================
df_filtre = df_score.copy()

if dep_choisi != "Tous":
    df_filtre = df_filtre[df_filtre["nom_dep"] == dep_choisi]

if commune_choisie != "Toutes":
    df_filtre = df_filtre[df_filtre["nom_commune"] == commune_choisie]

if priorite_choisie != "Toutes":
    df_filtre = df_filtre[df_filtre["priorite"] == priorite_choisie]

df_filtre = df_filtre[
    (df_filtre["score_potentiel"] >= score_min) &
    (df_filtre["score_potentiel"] <= score_max)
]

# Sécurité si aucun résultat
if df_filtre.empty:
    st.warning("Aucune commune ne correspond aux filtres sélectionnés.")
    st.stop()

# =========================
# KPI CARDS
# =========================
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Communes analysées", len(df_filtre))
col2.metric("Très prioritaires (A)", int((df_filtre["priorite"] == "A - tres prioritaire").sum()))
col3.metric("Score moyen", round(df_filtre["score_potentiel"].mean(), 2))
col4.metric("Total copropriétés", int(df_filtre["nb_copros"].fillna(0).sum()))
col5.metric("Total véhicules", int(df_filtre["nb_vehicules"].sum()))

# =========================
# CARTE
# =========================
df_map = df_filtre.dropna(subset=["lat", "long"]).copy()
df_map["nb_copros_size"] = pd.to_numeric(df_map["nb_copros"], errors="coerce").fillna(0).clip(lower=0) + 1

if df_map.empty:
    st.info("Aucune coordonnée géographique disponible pour afficher la carte.")
else:
    fig_map = px.scatter_map(
        df_map,
        lat="lat",
        lon="long",
        color="score_potentiel",
        size="nb_copros_size",
        hover_name="nom_commune",
        hover_data={
            "nom_dep": True,
            "score_potentiel": True,
            "priorite": True,
            "nb_copros": True,
            "nb_vehicules": True,
            "taux_motorisation": True,
            "lat": False,
            "long": False
        },
        zoom=5,
        height=600,
        title="Carte du potentiel commercial Parkshare"
    )
    st.plotly_chart(fig_map, use_container_width=True)

# =========================
# GRAPHIQUES
# =========================

st.subheader("Analyse du score selon une variable")

variables_x = [
    "population_totale",
    "nb_copros",
    "nb_vehicules",
    "taux_motorisation",
    "part_grandes_copros",
    "total_lots_stationnement",
    "ratio_stationnement_logements"
]

# Ajouter la colonne d'âge si elle existe
if "pop_15_29" in df_filtre.columns:
    variables_x.append("pop_15_29")

x_choisie = st.selectbox("Choisir la variable à comparer au score", variables_x)

# Taille de bulle robuste pour eviter les erreurs Plotly sur NaN
df_scatter = df_filtre.copy()
df_scatter["size_population"] = (
    pd.to_numeric(df_scatter["population_totale"], errors="coerce")
    .fillna(0)
    .clip(lower=0)
)
df_scatter["size_population"] = (df_scatter["size_population"] ** 0.5) + 1

fig_dynamic = px.scatter(
    df_scatter,
    x=x_choisie,
    y="score_potentiel",
    size="size_population",
    color="priorite",
    hover_name="nom_commune",
    title=f"Score potentiel en fonction de {x_choisie}"
)

st.plotly_chart(fig_dynamic, use_container_width=True)

colg1, colg2 = st.columns(2)

top10 = df_filtre.sort_values("score_potentiel", ascending=False).head(10)
fig_top10 = px.bar(
    top10,
    x="nom_commune",
    y="score_potentiel",
    color="priorite",
    title="Top 10 communes"
)
colg1.plotly_chart(fig_top10, use_container_width=True)

fig_segments = px.pie(
    df_filtre,
    names="priorite",
    title="Répartition des priorités"
)
colg2.plotly_chart(fig_segments, use_container_width=True)

colg3, colg4 = st.columns(2)

fig_scatter = px.scatter(
    df_scatter,
    x="nb_copros",
    y="score_potentiel",
    size="size_population",
    color="priorite",
    hover_name="nom_commune",
    title="Score vs nombre de copropriétés"
)
colg3.plotly_chart(fig_scatter, use_container_width=True)

df_dep = df_filtre.groupby("nom_dep", as_index=False).agg(
    score_moyen=("score_potentiel", "mean")
)
df_dep = df_dep.sort_values("score_moyen", ascending=False).head(15)

fig_dep = px.bar(
    df_dep,
    x="nom_dep",
    y="score_moyen",
    title="Score moyen par département"
)
colg4.plotly_chart(fig_dep, use_container_width=True)

# =========================
# TABLEAU DETAILLÉ
# =========================
st.subheader("Tableau détaillé")

cols_table = [
    "nom_commune",
    "nom_dep",
    "score_potentiel",
    "priorite",
    "nb_copros",
    "nb_vehicules",
    "population_totale",
    "taux_motorisation",
    "part_grandes_copros"
]

st.dataframe(
    df_filtre[cols_table].sort_values("score_potentiel", ascending=False),
    use_container_width=True
)