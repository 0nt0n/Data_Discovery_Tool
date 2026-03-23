import json
from dataclasses import asdict
from backend.connectors.sqlite import SqliteConnector
from backend.connectors.csv import CsvConnector
from .sensitivity import is_sensitive

SOURCES = [
    {
        "source_id": "main_db",
        "type": "sqlite",
        "path": "data/main.db"
    },
    {
        "source_id": "customers_csv",
        "type": "csv",
        "path": "data/customer_sample_500.csv",
    },
    {
        "source_id": "laptop_users_csv",
        "type": "csv",
        "path": "data/Laptop-Users.csv",
    }
]


def build_catalog():
    """Необхожимо добавить более безопасное использование"""
    catalog = {"sources": []}
    for source in SOURCES:
        if source["type"] == "sqlite":
            connector = SqliteConnector(
                source_id=source["source_id"], path=source["path"]
            )
        elif source["type"] == "csv":
            connector = CsvConnector(source_id=source["source_id"], path=source["path"])
        else:
            print("Uncorrect type connector")
            continue

        tables = connector.index_all()

        for table in tables:
            for column in table.columns:
                if is_sensitive(column.name):
                    column.is_sensitive = True

        catalog["sources"].append(
            {
                "source_id": source["source_id"],
                "type": source["type"],
                "tables": [asdict(t) for t in tables],
            }
        )

    with open("catalog.json", "w") as f:
        json.dump(catalog, f, indent=2)

    return catalog


def load_catalog():
    with open("catalog.json") as f:
        return json.load(f)
