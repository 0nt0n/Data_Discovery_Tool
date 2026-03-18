import pandas as pd
import os
from .base import BaseConnector, TableMeta, ColumnMeta


class CsvConnector(BaseConnector):
    def list_tables(self) -> list[str]:
        name = os.path.splitext(os.path.basename(self.path))[0]
        return [name]

    def get_table_meta(self, table: str) -> TableMeta:
        data = pd.read_csv(self.path)
        row_count = data.shape[0]
        columns = []
        for col in data.columns:
            dtype = str(data[col].dtype)
            if "int" in dtype:
                inferred = "integer"
            elif "float" in dtype:
                inferred = "float"
            else:
                inferred = "text"
            columns.append(
                ColumnMeta(
                    name=col,
                    dtype=inferred,
                    sample_values=data[col].dropna().unique()[:5].tolist(),
                )
            )
        preview = data.head(3).to_dict(orient="records")
        return TableMeta(
            name=table,
            source_id=self.source_id,
            row_count=row_count,
            columns=columns,
            preview=preview,
        )
