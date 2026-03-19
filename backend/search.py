from .catalog import load_catalog
from dataclasses import dataclass
from difflib import SequenceMatcher


@dataclass
class SearchResult:
    type: str
    score: float
    source_id: str
    table: str
    column: str
    preview: list


def search(query: str) -> list[SearchResult]:
    if not query:
        return []
    else:
        catalog = load_catalog()
        result = []
        for source in catalog["sources"]:
            source_id = source["source_id"]
            for table in source["tables"]:
                if query.lower() in table["name"].lower():
                    result.append(
                        SearchResult(
                            type="table",
                            score=1.0,
                            source_id=source_id,
                            table=table["name"],
                            column=None,
                            preview=table["preview"],
                        )
                    )
                else:
                    ratio = SequenceMatcher(
                        None, query.lower(), table["name"].lower()
                    ).ratio()
                    if ratio > 0.6:
                        result.append(
                            SearchResult(
                                type="table",
                                score=round(ratio * 0.8, 2),
                                source_id=source_id,
                                table=table["name"],
                                column=None,
                                preview=table["preview"],
                            )
                        )
                for column in table["columns"]:  # колонки внутри таблицы
                    if query.lower() in column["name"].lower():
                        result.append(
                            SearchResult(
                                type="column",
                                score=0.9,
                                source_id=source_id,
                                table=table["name"],
                                column=column["name"],
                                preview=table["preview"],
                            )
                        )
                    else:
                        ratio = SequenceMatcher(
                            None, query.lower(), column["name"].lower()
                        ).ratio()
                        if ratio > 0.6:
                            result.append(
                                SearchResult(
                                    type="column",
                                    score=round(ratio * 0.8, 2),
                                    source_id=source_id,
                                    table=table["name"],
                                    column=column["name"],
                                    preview=table["preview"],
                                )
                            )
                    for value in column["sample_values"]:
                        if query.lower() in str(value).lower():
                            result.append(
                                SearchResult(
                                    type="value",
                                    score=0.5,
                                    source_id=source["source_id"],
                                    table=table["name"],
                                    column=column["name"],
                                    preview=table["preview"],
                                )
                            )
                            break
        return sorted(result, key=lambda x: x.score, reverse=True)
