import logging
import pandas as pd
from sqlalchemy import create_engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


import os

def extract_from_source_db() -> pd.DataFrame:
    """Extrait les commandes depuis la base de données source de l'entreprise."""
    host = os.environ.get("SOURCE_DB_HOST", "localhost")
    port = os.environ.get("SOURCE_DB_PORT", "5433")
    url = f"postgresql+psycopg2://source_user:source_pass@{host}:{port}/ecommerce_source"
    engine = create_engine(url)

    df = pd.read_sql("SELECT * FROM orders", engine)
    logger.info("%d commandes extraites depuis la base source", len(df))
    return df

def extract_from_csv(csv_path: str) -> pd.DataFrame:
    """Extrait les données d'un export CSV simulant un système ERP."""
    logger.info("Extraction depuis le fichier CSV %s", csv_path)
    df = pd.read_csv(csv_path)
    logger.info("%d lignes extraites depuis le CSV", len(df))
    return df

if __name__ == "__main__":
    orders_df = extract_from_source_db()
    print(orders_df)

    csv_df = extract_from_csv("data/erp_export.csv")
    print(csv_df)