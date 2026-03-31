import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path


st.set_page_config(
    page_title="Parkshare - Prospection",
    page_icon="P",
    layout="wide",
)

PRIORITY_COLORS = {
    "A - tres prioritaire": "#08306B",
    "B - prioritaire": "#2171B5",
    "C - secondaire": "#6BAED6",
    "D - faible priorite": "#C6DBEF",
}


@st.cache_data
def load_data() -> pd.DataFrame:
    app_dir = Path(__file__).resolve().parent
    data_path = app_dir.parent / "data" / "Sources_clean" / "kpi_potentiel_communes.csv"
    if not data_path.exists():
        raise FileNotFoundError(f"Fichier KPI introuvable: {data_path}")

    df = pd.read_csv(data_path, low_memory=False)

    numeric_cols = [
        "score_potentiel",
        "rang_potentiel",
        "score_demande",
        "score_copro",
        "score_parking",
        "nb_copros",
        "nb_vehicules",
        "population_totale",
        "total_lots_stationnement",
        "nb_points_parking",
        "lat",
        "long",
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Colonnes utiles pour visualisation
    df["taux_motorisation"] = df["nb_vehicules"] / df["population_totale"].replace(0, pd.NA)
    df["size_population"] = (df["population_totale"].fillna(0).clip(lower=0) ** 0.5) + 1
    df["size_copro"] = (df["nb_copros"].fillna(0).clip(lower=0) ** 0.5) + 1

    # Echelle de taille robuste: limite l'impact des valeurs extremes.
    score_clean = df["score_potentiel"].fillna(0).clip(lower=0)
    q_low = float(score_clean.quantile(0.10))
    q_high = float(score_clean.quantile(0.90))
    if q_high > q_low:
        score_clipped = score_clean.clip(lower=q_low, upper=q_high)
        score_scaled = (score_clipped - q_low) / (q_high - q_low)
    else:
        score_scaled = pd.Series(0.5, index=df.index)
    # Taille plus compacte pour rester lisible en vue dezoom.
    df["size_score_map"] = 3 + (score_scaled * 10)

    return df


def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.header("Filtres")

    deps = ["Tous"] + sorted(df["nom_dep"].dropna().unique().tolist())
    dep_choisi = st.sidebar.selectbox("Departement", deps)

    df_temp = df.copy()
    if dep_choisi != "Tous":
        df_temp = df_temp[df_temp["nom_dep"] == dep_choisi]

    communes = ["Toutes"] + sorted(df_temp["nom_commune"].dropna().unique().tolist())
    commune_choisie = st.sidebar.selectbox("Commune", communes)

    priorites = ["Toutes"] + sorted(df["priorite"].dropna().unique().tolist())
    priorite_choisie = st.sidebar.selectbox("Priorite", priorites)

    score_min, score_max = st.sidebar.slider(
        "Score potentiel",
        float(df["score_potentiel"].min()),
        float(df["score_potentiel"].max()),
        (
            float(df["score_potentiel"].quantile(0.20)),
            float(df["score_potentiel"].max()),
        ),
    )

    df_filtre = df.copy()
    if dep_choisi != "Tous":
        df_filtre = df_filtre[df_filtre["nom_dep"] == dep_choisi]
    if commune_choisie != "Toutes":
        df_filtre = df_filtre[df_filtre["nom_commune"] == commune_choisie]
    if priorite_choisie != "Toutes":
        df_filtre = df_filtre[df_filtre["priorite"] == priorite_choisie]

    df_filtre = df_filtre[
        (df_filtre["score_potentiel"] >= score_min)
        & (df_filtre["score_potentiel"] <= score_max)
    ]

    return df_filtre


def main() -> None:
    st.title("Parkshare - Dashboard de priorisation commerciale")
    st.caption(
        "Objectif: identifier rapidement les communes les plus pertinentes pour la prospection syndics et bailleurs."
    )

    try:
        df = load_data()
    except Exception as exc:
        st.error(str(exc))
        st.stop()

    df_filtre = apply_filters(df)
    if df_filtre.empty:
        st.warning("Aucune commune ne correspond aux filtres selectionnes.")
        st.stop()

    # KPI priorites
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Communes ciblees", f"{len(df_filtre):,}".replace(",", " "))
    c2.metric(
        "Priorite A",
        int((df_filtre["priorite"] == "A - tres prioritaire").sum()),
    )
    c3.metric("Score moyen", round(df_filtre["score_potentiel"].mean(), 2))
    c4.metric("Coproprietes totales", int(df_filtre["nb_copros"].fillna(0).sum()))
    c5.metric("Lots stationnement", int(df_filtre["total_lots_stationnement"].fillna(0).sum()))

    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(
        ["Carte des opportunites", "Analyse et priorisation", "Table des communes"]
    )

    with tab1:
        st.subheader("Carte des opportunites par commune")
        df_map = df_filtre.dropna(subset=["lat", "long"]).copy()
        if df_map.empty:
            st.info("Aucune donnee geographique exploitable apres filtrage.")
        else:
            fig_map = px.scatter_map(
                df_map,
                lat="lat",
                lon="long",
                color="score_potentiel",
                size="size_score_map",
                size_max=14,
                hover_name="nom_commune",
                hover_data={
                    "nom_dep": True,
                    "score_potentiel": True,
                    "priorite": True,
                    "nb_copros": True,
                    "population_totale": True,
                    "total_lots_stationnement": True,
                    "lat": False,
                    "long": False,
                },
                zoom=4.5,
                height=620,
                title="Potentiel commercial Parkshare",
                color_continuous_scale="Blues",
            )
            fig_map.update_traces(marker={"opacity": 0.65})
            st.plotly_chart(fig_map, use_container_width=True)

    with tab2:
        left, right = st.columns(2)

        top15 = df_filtre.sort_values("score_potentiel", ascending=False).head(15)
        fig_top = px.bar(
            top15,
            x="nom_commune",
            y="score_potentiel",
            color="priorite",
            title="Top 15 communes a prospecter",
            color_discrete_map=PRIORITY_COLORS,
        )
        left.plotly_chart(fig_top, use_container_width=True)

        dep_scores = (
            df_filtre.groupby("nom_dep", as_index=False)["score_potentiel"]
            .mean()
            .sort_values("score_potentiel", ascending=False)
            .head(15)
        )
        fig_dep = px.bar(
            dep_scores,
            x="nom_dep",
            y="score_potentiel",
            title="Top 15 departements (score moyen)",
        )
        right.plotly_chart(fig_dep, use_container_width=True)

        st.subheader("Composantes du score")
        x_var = st.selectbox(
            "Variable a comparer au score",
            [
                "population_totale",
                "nb_vehicules",
                "nb_copros",
                "total_lots_stationnement",
                "taux_motorisation",
            ],
        )
        fig_scatter = px.scatter(
            df_filtre,
            x=x_var,
            y="score_potentiel",
            size="size_population",
            color="priorite",
            hover_name="nom_commune",
            title=f"Score potentiel selon {x_var}",
            color_discrete_map=PRIORITY_COLORS,
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    with tab3:
        st.subheader("Table detaillee des communes")
        cols = [
            "code_insee",
            "code_postal",
            "nom_commune",
            "nom_dep",
            "score_potentiel",
            "rang_potentiel",
            "priorite",
            "score_demande",
            "score_copro",
            "score_parking",
            "population_totale",
            "nb_vehicules",
            "nb_copros",
            "total_lots_stationnement",
            "lat",
            "long",
        ]
        out = df_filtre[cols].sort_values("score_potentiel", ascending=False)
        st.dataframe(out, use_container_width=True, hide_index=True)
        st.download_button(
            label="Exporter le resultat filtre (CSV)",
            data=out.to_csv(index=False).encode("utf-8"),
            file_name="prospection_filtree.csv",
            mime="text/csv",
        )


if __name__ == "__main__":
    main()
