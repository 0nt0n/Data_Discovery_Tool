import pytest
from pathlib import Path
from backend.connectors.sqlite import SqliteConnector
from backend.connectors.csv import CsvConnector


DATA_DIR = Path(__file__).parent.parent / "data"


def test_sqlite_list_tables():
    c = SqliteConnector("main_db", str(DATA_DIR / "main.db"))
    tables = c.list_tables()
    assert len(tables) > 0


def test_sqlite_table_meta():
    c = SqliteConnector("netflix_db", str(DATA_DIR / "main.db"))
    meta = c.get_table_meta("users")
    assert meta.row_count > 10
    assert len(meta.columns) > 0
    assert len(meta.preview) == 3


def test_sqlite_sample_values():
    c = SqliteConnector("netflix_db", str(DATA_DIR / "main.db"))
    meta = c.get_table_meta("users")
    country_col = next(c for c in meta.columns if c.name == "country")
    assert len(country_col.sample_values) > 0


def test_csv_list_tables():
    c = CsvConnector("customers_csv", str(DATA_DIR / "customer_sample_500.csv"))
    tables = c.list_tables()
    assert tables == ["customer_sample_500"]


def test_csv_table_meta():
    c = CsvConnector("customers_csv", str(DATA_DIR / "customer_sample_500.csv"))
    meta = c.get_table_meta("customer_sample_500")
    assert meta.row_count > 100
    assert len(meta.columns) > 0
    assert len(meta.preview) == 3
