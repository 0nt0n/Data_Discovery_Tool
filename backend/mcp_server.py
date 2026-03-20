from fastapi import FastAPI, Query
from .catalog import load_catalog, build_catalog
from .search import search
from dataclasses import asdict
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/sources")
def listSources():
    catalog = load_catalog()
    return {
        "sources": [
            {
                "source_id": source["source_id"],
                "type": source["type"],
                "Count_tables": len(source["tables"]),
            }
            for source in catalog["sources"]
        ]
    }


@app.post("/index")
def indexSource(source_id: str = Query(default=None)):
    build_catalog()
    return {"status": "ok"}


@app.get("/search")
def search_finally(q: str = None):
    if not q:
        return []
    results = search(query=q)
    return [asdict(r) for r in results]


@app.get("/schema/{source_id}/{table}")
def get_schema(source_id: str, table: str):
    catalog = load_catalog()
    for source in catalog["sources"]:
        if source_id == source["source_id"]:
            for t in source["tables"]:
                if table == t["name"]:
                    return t
    return {"error": "not found"}
