import sqlite3
from .base import BaseConnector, TableMeta, ColumnMeta


class SqliteConnector(BaseConnector):
    def list_tables(self) -> list[str]:
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            rows = cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
        return [r[0] for r in rows]

    def get_table_meta(self, table: str) -> TableMeta:
        with sqlite3.connect(self.path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            row_count = cursor.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]

            preview_rows = cursor.execute(f"SELECT * FROM {table} LIMIT 3").fetchall()
            preview = [dict(r) for r in preview_rows]

            columns = []
            cols_info = cursor.execute(f"PRAGMA table_info({table})").fetchall()
            for col in cols_info:
                samples = cursor.execute(
                    f"SELECT DISTINCT {col['name']} FROM {table} "
                    f"WHERE {col['name']} IS NOT NULL LIMIT 5"
                ).fetchall()
                columns.append(
                    ColumnMeta(
                        name=col["name"],
                        dtype=col["type"].lower() or "text",
                        nullable=not col["notnull"],
                        sample_values=[r[0] for r in samples],
                    )
                )

        return TableMeta(
            name=table,
            source_id=self.source_id,
            row_count=row_count,
            columns=columns,
            preview=preview,
        )
