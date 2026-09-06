
import sys

import pandas as pd
import pytest

sys.path.append("../src")
sys.path.append("src")

from transform import (
    _validate_no_nulls,
    clean_product_catalog,
    transform_orders_from_csv,
    transform_orders_from_db,
)


def test_transform_orders_from_db_computes_total_amount():
    df = pd.DataFrame(
        {
            "order_id": ["ORD-1"],
            "customer_id": [101],
            "product_id": [1],
            "quantity": [3],
            "unit_price": [10.0],
            "order_date": ["2026-08-01"],
        }
    )
    result = transform_orders_from_db(df)
    assert result.loc[0, "total_amount"] == 30.0
    assert result.loc[0, "source_system"] == "crm_db"


def test_transform_orders_from_csv_renames_columns():
    df = pd.DataFrame(
        {
            "OrderID": ["ORD-2"],
            "CustomerID": [202],
            "ProductID": [5],
            "Qty": [2],
            "Price": [20.0],
            "Date": ["2026-08-02"],
        }
    )
    result = transform_orders_from_csv(df)
    assert "order_id" in result.columns
    assert result.loc[0, "total_amount"] == 40.0
    assert result.loc[0, "source_system"] == "csv"


def test_validate_no_nulls_raises_on_missing_data():
    df = pd.DataFrame({"order_id": ["ORD-3", None], "quantity": [1, 2]})
    with pytest.raises(ValueError):
        _validate_no_nulls(df, ["order_id", "quantity"])


def test_clean_product_catalog_strips_and_renames():
    df = pd.DataFrame(
        {
            "id": [1],
            "title": ["  T-shirt  "],
            "category": ["clothing"],
            "price": [19.99],
        }
    )
    result = clean_product_catalog(df)
    assert result.loc[0, "product_name"] == "T-shirt"
    assert "product_id" in result.columns
