# Pipeline ETL — Centralisation des ventes e-commerce

## Contexte métier

Une entreprise de retail reçoit des données de ventes depuis deux systèmes
différents :
- une **base de données transactionnelle** (CRM) enregistrant les commandes,
- des **exports CSV** provenant de son système ERP.

Ces données, dispersées et dans des formats différents, empêchent toute
analyse consolidée. Ce projet construit un pipeline **ETL** (Extract,
Transform, Load) qui centralise ces sources dans un **data warehouse**
unique, orchestré par Apache Airflow.

## Architecture

<img width="541" height="397" alt="image" src="https://github.com/user-attachments/assets/fc642fd7-d92e-402e-8140-358afd6c5c84" />



- **Orchestration** : Apache Airflow (DAG déclenchable manuellement ou planifié quotidiennement)
- **Transformation** : Python / pandas — harmonisation des deux sources vers un schéma commun
- **Stockage cible** : PostgreSQL (table `fact_sales` + dimensions `dim_product`, `dim_customer`)
- **Conteneurisation** : Docker Compose (3 bases Postgres + Airflow), environnement reproductible en une commande

## Pourquoi ces choix

| Décision | Raison |
|---|---|
| Airflow plutôt qu'un script exécuté manuellement | Visibilité sur les exécutions, retries automatiques, planification |
| Chargement idempotent (DELETE puis INSERT par `order_id`) | Relancer le pipeline plusieurs fois ne crée jamais de doublons |
| Connexions DB configurables via variables d'environnement | Le même code fonctionne en local (`localhost`) et dans Airflow (nom de service Docker) |
| Séparation extract / transform / load en modules distincts | Code testable indépendamment, logique claire |

## Démarrage rapide

```bash
git clone <repo>
cd ecommerce-etl-pipeline
docker compose up -d
```

- Interface Airflow : http://localhost:8081 (admin / admin)
- Base source (CRM) : `localhost:5433`
- Data warehouse : `localhost:5434`

Le DAG `sales_etl_pipeline` peut être déclenché manuellement depuis l'interface Airflow, ou s'exécute automatiquement chaque jour.

## Structure du projet
