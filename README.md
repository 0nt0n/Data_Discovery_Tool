# Data Discovery Tool

Инструмент для поиска и обнаружения данных across нескольких источников. Поддерживает MCP (Model Context Protocol) — AI агент может вызывать инструменты поиска напрямую.

## Источники данных

- `data/main.db` — SQLite база данных с таблицами: `users`, `social_media_users`
- `data/customer_sample_500.csv` — CSV с 500 записями клиентов
- `data/products.csv` — CSV с 200 записями продуктов

## Установка

### Требования
- Python 3.10+

### Шаги
```bash
# клонируй репозиторий
git clone <repo_url>
cd Data_Discovery_Tool

# создай виртуальное окружение
python3 -m venv venv
source venv/bin/activate  # Mac/Linux

# установи зависимости
pip install -r requirements.txt
```

### requirements.txt
```
fastapi
uvicorn
pandas
httpx
pytest
```

## Запуск

**1. Построить каталог (проиндексировать все источники):**
```bash
python3 -c "from backend.catalog import build_catalog; build_catalog()"
```

**2. Запустить сервер:**
```bash
uvicorn backend.mcp_server:app --reload
```

**3. Открыть UI:**
```
Открыть frontend/index.html в браузере
```

**4. Документация API:**
```
http://localhost:8000/docs
```

## Запуск тестов
```bash
pytest tests/ -v
```

## Структура проекта
```
Data_Discovery_Tool/
├── backend/
│   ├── connectors/
│   │   ├── base.py         # абстрактный интерфейс коннектора
│   │   ├── sqlite.py       # коннектор для SQLite
│   │   └── csv.py          # коннектор для CSV
│   ├── catalog.py          # построение и загрузка каталога
│   ├── search.py           # keyword + fuzzy поиск
│   ├── sensitivity.py      # определение чувствительных данных
│   └── mcp_server.py       # FastAPI MCP сервер
├── frontend/
│   └── index.html          # UI для поиска
├── data/                   # источники данных
├── tests/                  # pytest тесты
├── catalog.json            # сгенерированный индекс
└── README.md
```

## MCP Эндпоинты

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| GET | `/sources` | Список всех источников данных |
| POST | `/index` | Пересобрать каталог |
| GET | `/search?q=запрос` | Поиск по всем источникам |
| GET | `/schema/{source_id}/{table}` | Схема конкретной таблицы |

## Дизайн решения

- **Архитектура** — три слоя: коннекторы → каталог → поиск. Каждый слой независим.
- **Расширяемость** — новый источник данных = новый файл коннектора, остальное не трогать.
- **Поиск** — keyword + fuzzy (SequenceMatcher). Находит результаты даже при опечатках.
- **Чувствительные данные** — автоматическая пометка колонок (email, age, income, name и др.)
