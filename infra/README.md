# Infrastructure Parkshare

Ce dossier contient l'ensemble de la configuration nécessaire au déploiement de la stack technique du projet Parkshare. L'architecture est conçue pour être contenerisée, isolée et sécurisée via un certificat SSL.

## Point clés de l'infrastructure
* Sécurité SSL/TLS
* Reverse Proxy
* Orchestration Docker
* Routage réseau

## Pré-requis
* **Docker** et **Docker Compose** installés sur la machine hôte.
* Accès réseau configuré (Port 80 (HTTP) et 443 (HTTPS)).

## Structure du dossier
```bash
/home/parkshare/
├── app/       
└── infra/            
   ├── docker-compose.yml  
   ├── nginx.conf          
   ├── .env.example            
   └── certs/              
```


## Déploiement Rapide

1. **Préparer le .env :**
   ```bash
   cp .env.example .env

2. **Créer le dossier certs**
   ```bash
   mkdir certs

3. **Générer les certificats**
   ```bash
   openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout certs/nginx.key -out certs/nginx.crt

4. **Lancer le build :**
    ```bash
    docker-compose up -d --build