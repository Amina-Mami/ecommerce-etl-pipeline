import logging
import os

import pandas as pd
from sqlalchemy import create_engine, text

logger = logging.getLogger(__name__)


def load_fact_sales(df: pd.DataFrame) -> None:
    """Charge les ventes harmonisées dans fact_sales, sans créer de doublons."""
    host = os.environ.get("DWH_DB_HOST", "localhost")
    port = os.environ.get("DWH_DB_PORT", "5434")
    url = f"postgresql+psycopg2://dwh_user:dwh_pass@{host}:{port}/ecommerce_dwh"
    engine = create_engine(url)

    order_ids = tuple(df["order_id"].unique())

    with engine.begin() as conn:
        # 1. On supprime les anciennes versions de ces commandes (si elles existent)
        if order_ids:
            conn.execute(
                text("DELETE FROM fact_sales WHERE order_id IN :ids").bindparams(
                    ids=order_ids
                )
            )

        # 2. On insère la version à jour
        df.to_sql("fact_sales", conn, if_exists="append", index=False)

    logger.info("%d lignes chargées dans fact_sales (idempotent)", len(df))


if __name__ == "__main__":
    from extract import extract_from_source_db
    from transform import transform_orders_from_db

    raw = extract_from_source_db()
    transformed = transform_orders_from_db(raw)
    load_fact_sales(transformed)