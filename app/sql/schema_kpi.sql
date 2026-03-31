PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS kpi_potentiel_communes (
    kpi_id INTEGER PRIMARY KEY AUTOINCREMENT,
    code_insee TEXT NOT NULL,
    code_postal TEXT,
    nom_commune TEXT,
    nom_dep TEXT,
    lat REAL,
    long REAL,
    score_potentiel REAL,
    rang_potentiel INTEGER,
    priorite TEXT,
    score_demande REAL,
    score_copro REAL,
    score_parking REAL,
    data_completeness REAL,
    coef_completeness REAL,
    coef_ruralite REAL,
    population_totale INTEGER,
    nb_vehicules INTEGER,
    nb_vp_elec INTEGER,
    nb_copros INTEGER,
    nb_logements INTEGER,
    grandes_copros_nb INTEGER,
    part_grandes_copros REAL,
    total_lots_stationnement INTEGER,
    moyenne_lots_par_point REAL,
    nb_points_parking INTEGER,
    source_file TEXT NOT NULL,
    loaded_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_kpi_communes_code_insee
ON kpi_potentiel_communes (code_insee);

CREATE INDEX IF NOT EXISTS idx_kpi_communes_priorite
ON kpi_potentiel_communes (priorite);

CREATE INDEX IF NOT EXISTS idx_kpi_communes_score
ON kpi_potentiel_communes (score_potentiel);
