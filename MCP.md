# MCP (Model Context Protocol)

## Манифест
```json
{
  "name": "data-discovery",
  "version": "1.0",
  "description": "Search and discover data across multiple sources",
  "tools": [
    {
      "name": "listSources",
      "description": "List all available data sources",
      "endpoint": "GET /sources"
    },
    {
      "name": "indexSource", 
      "description": "Rebuild the catalog index",
      "endpoint": "POST /index"
    },
    {
      "name": "search",
      "description": "Search across all data sources by keyword",
      "endpoint": "GET /search?q={query}"
    },
    {
      "name": "getSchema",
      "description": "Get full schema for a specific table",
      "endpoint": "GET /schema/{source_id}/{table}"
    }
  ]
}
```

## Эндпоинты

### GET /sources
Возвращает список всех источников данных.

**Запрос:**
```
GET http://localhost:8000/sources
```

**Ответ:**
```json
{
  "sources": [
    {"source_id": "main_db", "type": "sqlite", "tables_count": 2},
    {"source_id": "customers_csv", "type": "csv", "tables_count": 1}
  ]
}
```

---

### POST /index
Пересобирает каталог — переиндексирует все источники.

**Запрос:**
```
POST http://localhost:8000/index
```

**Ответ:**
```json
{"status": "ok"}
```

---

### GET /search
Поиск по всем источникам. Возвращает ранжированные результаты.

**Запрос:**
```
GET http://localhost:8000/search?q=country
```

**Ответ:**
```json
[
  {
    "type": "column",
    "score": 0.9,
    "source_id": "main_db",
    "table": "users",
    "column": "country",
    "preview": [
      {"user_id": 1, "name": "James", "country": "France"}
    ]
  }
]
```

**Типы результатов:**
- `table` — совпадение в имени таблицы (score 1.0)
- `column` — совпадение в имени колонки (score 0.9)
- `value` — совпадение в sample values (score 0.5)
- fuzzy — нечёткое совпадение (score 0.3-0.8)

---

### GET /schema/{source_id}/{table}
Возвращает полную схему таблицы.

**Запрос:**
```
GET http://localhost:8000/schema/main_db/users
```

**Ответ:**
```json
{
  "name": "users",
  "source_id": "main_db",
  "row_count": 100,
  "columns": [
    {
      "name": "country",
      "dtype": "text",
      "sample_values": ["France", "USA", "UK"],
      "nullable": true,
      "is_sensitive": false
    }
  ],
  "preview": [
    {"user_id": 1, "name": "James", "country": "France"}
  ]
}
```

## Типичный сценарий агента
```
1. GET /sources           → узнать какие источники есть
2. GET /search?q=country  → найти релевантные таблицы
3. GET /schema/main_db/users → получить полную схему
4. агент принимает решение что делать с данными
```