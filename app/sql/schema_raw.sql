PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS raw_aaa_opendata_rechargeable (
    ingest_id INTEGER PRIMARY KEY AUTOINCREMENT,
    codgeo TEXT,
    libgeo TEXT,
    epci TEXT,
    libepci TEXT,
    date_arrete TEXT,
    nb_vp_rechargeables_el TEXT,
    nb_vp_rechargeables_gaz TEXT,
    nb_vp TEXT,
    source_file TEXT NOT NULL,
    loaded_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS raw_tableau_synthetique_coproff (
    ingest_id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_reg TEXT,
    code_reg TEXT,
    nom_dep TEXT,
    code_dep TEXT,
    code_epci TEXT,
    nom_epci TEXT,
    code_com TEXT,
    nom_commune TEXT,
    nb_copros TEXT,
    nb_logements TEXT,
    copros_5_moins TEXT,
    copros_6_10 TEXT,
    copros_11_20 TEXT,
    copros_21_50 TEXT,
    copros_51_200 TEXT,
    copros_200_plus TEXT,
    copros_avant_49 TEXT,
    copros_49_74 TEXT,
    copros_75_2000 TEXT,
    copros_2000_plus TEXT,
    copros_annee_na TEXT,
    taux_immat TEXT,
    source_file TEXT NOT NULL,
    loaded_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS raw_population_insee (
    ingest_id INTEGER PRIMARY KEY AUTOINCREMENT,
    code_insee TEXT,
    population_totale TEXT,
    pop_15_29 TEXT,
    pop_60_74 TEXT,
    pop_75_89 TEXT,
    pop_90_plus TEXT,
    residences_principales TEXT,
    logements_vacants TEXT,
    logements_locatifs TEXT,
    pop_sans_diplome TEXT,
    pop_bac TEXT,
    pop_bac_plus_2 TEXT,
    pop_bac_plus_5 TEXT,
    pop_active TEXT,
    pop_chomeurs TEXT,
    pop_inactifs TEXT,
    revenu_median TEXT,
    taux_pauvrete TEXT,
    nb_beneficiaires_rsa TEXT,
    nb_allocataires_minimum_vieillesse TEXT,
    nb_allocataires_famille TEXT,
    nb_minima_sociaux TEXT,
    nb_aides_logement TEXT,
    source_file TEXT NOT NULL,
    loaded_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS raw_mapping (
    ingest_id INTEGER PRIMARY KEY AUTOINCREMENT,
    code_insee TEXT,
    code_postal TEXT,
    nom_commune TEXT,
    departement TEXT,
    source_file TEXT NOT NULL,
    loaded_at TEXT NOT NULL DEFAULT (datetime('now'))
);
