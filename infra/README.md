# Infrastructure Parkshare

Ce dossier contient toute la configuration nécessaire pour déployer la stack technique du projet Parkshare de manière conteneurisée et sécurisée.

## Pré-requis
* **Docker** et **Docker Compose** installés sur la machine hôte.
* Accès réseau configuré (NAT/Redirection de port 80).

## Structure du dossier
* `docker-compose.yml` : Orchestration des services (Application + Base de données SQLite).
* `.env.example` : Modèle des variables d'environnement nécessaires.
* `data/` : Volume persistant pour la base de données SQLite.

## Déploiement Rapide

1. **Préparer le .env :**
   ```bash
   cp .env.example .env
