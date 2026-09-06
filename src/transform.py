
import logging
import pandas as pd

logger = logging.getLogger(__name__)

TARGET_COLUMNS = [
    "order_id",
    "product_id",
    "customer_id",
    "quantity",
    "unit_price",
    "total_amount",
    "sale_date",
    "source_system",
]


def transform_orders_from_db(orders_df: pd.DataFrame) -> pd.DataFrame:
    """Harmonise les commandes issues de la base source vers le schéma cible."""
    df = orders_df.copy()

    
    df["total_amount"] = df["quantity"] * df["unit_price"]

    
    df["source_system"] = "crm_db"

  
    df = df.rename(columns={"order_date": "sale_date"})

    return df[TARGET_COLUMNS]

def transform_orders_from_csv(csv_df: pd.DataFrame) -> pd.DataFrame:
    """Harmonise un export CSV (colonnes ERP) vers le schéma cible."""
    df = csv_df.copy()

    df = df.rename(columns={
        "OrderID": "order_id",
        "ProductID": "product_id",
        "CustomerID": "customer_id",
        "Qty": "quantity",
        "Price": "unit_price",
        "Date": "sale_date",
    })

    df["total_amount"] = df["quantity"] * df["unit_price"]
    df["source_system"] = "csv"

    return df[TARGET_COLUMNS]


if __name__ == "__main__":
    from extract import extract_from_source_db, extract_from_csv

    raw_db = extract_from_source_db()
    print(transform_orders_from_db(raw_db))

    raw_csv = extract_from_csv("data/erp_export.csv")
    print(transform_orders_from_csv(raw_csv))