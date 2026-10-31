
from pathlib import Path

import pandas as pd
from sqlalchemy import text

from app.database.connection import engine


REQUIRED_COLUMNS = [
    "Transaction_Id",
    "Order_date",
    "Product",
    "Category",
    "Region",
    "Sales_channel",
    "Quantity",
    "Unit_price",
    "Discount_amount",
    "Status"
]


def load_sales_data(csv_path: str):

    # 1. Read CSV
    df = pd.read_csv(csv_path)

    # 2. Validate required columns
    missing_columns = set(REQUIRED_COLUMNS) - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing columns: {missing_columns}"
        )

    # 3. Normalize column names
    df.columns = df.columns.str.strip().str.lower()

    df = df.rename(columns={
        "transaction_id": "transaction_id",
        "order_date": "order_date",
        "sales_channel": "sales_channel",
        "unit_price": "unit_price",
        "discount_amount": "discount_amount"
    })

    # 4. Remove duplicate transactions
    total_records = len(df)

    df = df.drop_duplicates(
        subset=["transaction_id"],
        keep="first"
    )

    # 5. Clean string columns
    string_columns = [
        "transaction_id",
        "product",
        "category",
        "region",
        "sales_channel",
        "status"
    ]

    for column in string_columns:
        df[column] = df[column].astype("string").str.strip()
    for column in string_columns:
        df[column] = df[column].replace("", pd.NA)

    # 6. Convert date and numeric columns
    df["order_date"] = pd.to_datetime(
        df["order_date"],
        format="%d-%m-%Y",
        errors="coerce"
    )

    for column in [
        "quantity",
        "unit_price",
        "discount_amount"
    ]:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # 7. Identify invalid records
    required_values = [
        "transaction_id",
        "order_date",
        "product",
        "category",
        "region",
        "sales_channel",
        "status",
        "quantity",
        "unit_price",
        "discount_amount"
    ]

    invalid_mask = df[required_values].isna().any(axis=1)

    invalid_mask |= df["quantity"] <= 0
    invalid_mask |= df["unit_price"] <= 0
    invalid_mask |= df["discount_amount"] < 0

    invalid_mask |= (
        df["discount_amount"]
        > df["quantity"] * df["unit_price"]
    )

    invalid_count = int(invalid_mask.sum())

    # 8. Keep valid records
    df = df.loc[~invalid_mask].copy()

    # 9. Format dates
    df["order_date"] = df["order_date"].dt.strftime(
        "%Y-%m-%d"
    )

    # 10. Calculate revenue
    df["revenue"] = (
        df["quantity"] * df["unit_price"]
        - df["discount_amount"]
    )

    # 11. Convert column names to database format
    df.columns = df.columns.str.lower()

    # 12. Load into SQLite
    df.to_sql(
        "sales_transactions",
        con=engine,
        if_exists="replace",
        index=False
    )

    # 13. Create useful indexes
    with engine.begin() as connection:
        connection.execute(text("""
            CREATE UNIQUE INDEX IF NOT EXISTS
            idx_transaction_id
            ON sales_transactions(transaction_id)
        """))

        connection.execute(text("""
            CREATE INDEX IF NOT EXISTS
            idx_order_date
            ON sales_transactions(order_date)
        """))

        connection.execute(text("""
            CREATE INDEX IF NOT EXISTS
            idx_product
            ON sales_transactions(product)
        """))

        connection.execute(text("""
            CREATE INDEX IF NOT EXISTS
            idx_region
            ON sales_transactions(region)
        """))

    # 14. Return ingestion summary
    return {
        "total_records": total_records,
        "valid_records": len(df),
        "invalid_records": invalid_count,
        "returned_records": int(
            (df["status"].str.lower() == "returned").sum()
        ),
        "loaded_into_database": True
    }
