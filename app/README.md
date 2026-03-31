# Parkshare - App

Dashboard Streamlit de priorisation commerciale (communes) base sur les KPI de la base de donnée sqlite `db/parkshare_kpi.db`.

## Contenu

- `dashboard.py` : application Streamlit (filtres + carte + analyses).
- `sql/schema_raw.sql` : schema de la base brute.
- `sql/schema_kpi.sql` : schema de la base KPI.
- `raw_db_setup.ipynb` : creation/alimentation de `db/parkshare_raw.db`.
- `kpi_db_setup.ipynb` : creation/alimentation de `db/parkshare_kpi.db`.

## Lancer le dashboard

Depuis le dossier `app/` :

```bash
streamlit run dashboard.py
```

## Initialiser les bases SQLite

1. Ouvrir et executer `raw_db_setup.ipynb` pour charger les sources brutes.
2. Ouvrir et executer `kpi_db_setup.ipynb` pour charger **100%** des lignes KPI.

Les bases generees sont dans `app/db/`.
