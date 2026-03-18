import json
from dataclasses import asdict
from backend.connectors.sqlite import SqliteConnector
from backend.connectors.csv import CsvConnector

SOURCES = [
    {"source_id": "netflix_db", "type": "sqlite", "path": "data/netflix.db"},
    {
        "source_id": "customers_csv",
        "type": "csv",
        "path": "data/customer_sample_500.csv",
    },
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

        tables = connector.index_all()

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
