from pathlib import Path

from app.database.connection import check_database
from app.services.data_loader import load_sales_data


def initialize_database():
    project_root = Path(__file__).resolve().parents[2]

    csv_path = project_root / "data" / "sales_data.csv"

    if not csv_path.exists():
        raise FileNotFoundError(
            f"Sales CSV not found: {csv_path}"
        )

    if not check_database():
        raise RuntimeError("Database connection failed")

    result = load_sales_data(str(csv_path))

    print("\nDatabase initialization completed!")
    print(result)


if __name__ == "__main__":
    initialize_database()