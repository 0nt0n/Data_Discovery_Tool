from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ColumnMeta:
    """Класс описывающий колонку"""

    name: str
    dtype: str
    sample_values: list[Any] = field(default_factory=list)
    nullable: bool = True
    is_sensitive: bool = False


@dataclass
class TableMeta:
    """Класс описывающий таблицу"""

    name: str
    source_id: str
    row_count: int
    columns: list[ColumnMeta]
    preview: list[dict] = field(default_factory=list)


class BaseConnector(ABC):
    """Абстрактный класс для последующей реализации коннекторов
    можно назвать шаблоном)"""

    def __init__(self, source_id: str, path: str):
        self.source_id = source_id
        self.path = path

    @abstractmethod
    def list_tables(self) -> list[str]:
        """Вернуть список таблиц/листов в источнике"""
        ...

    @abstractmethod
    def get_table_meta(self, table: str) -> TableMeta:
        """Вернуть полные метаданные одной таблицы"""
        ...

    def index_all(self) -> list[TableMeta]:
        """Проиндексировать все таблицы — вызывается catalog.py"""
        return [self.get_table_meta(t) for t in self.list_tables()]
