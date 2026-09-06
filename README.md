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



## Difficultés rencontrées et résolues

- **Conflit de dépendances Airflow** : forcer une version récente de SQLAlchemy dans `requirements.txt` cassait Airflow en interne (qui a besoin de SQLAlchemy < 2.0). Résolu en ne pinnant que les dépendances sans conflit.
- **Conflit de port** : le port 8080 était déjà utilisé par un autre service local — Airflow a été redirigé sur le port 8081.
- **Résolution réseau Docker** : les scripts Python doivent utiliser `localhost` en local mais le nom du service Docker (`source-db`, `dwh-db`) depuis Airflow. Résolu avec des variables d'environnement à valeur par défaut.
- **Idempotence** : le chargement initial en `append` créait des doublons à chaque nouvelle exécution du DAG. Résolu avec un `DELETE` ciblé par `order_id` avant chaque `INSERT`.

## Pistes d'amélioration

- Ajouter une 3e source (API produits) pour peupler `dim_product`
- Ajouter des tests unitaires sur les fonctions de transformation
- Ajouter un dashboard BI (Metabase) connecté au data warehouse
- CI/CD avec GitHub Actions

