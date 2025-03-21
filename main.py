# from fastapi import FastAPI, Request
# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates
# import uvicorn

# app = FastAPI()

# # Define the templates directory
# templates = Jinja2Templates(directory="templates")

# @app.get("/", response_class=HTMLResponse)
# async def read_root(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})

# @app.post("/insert", response_class=HTMLResponse)
# async def insert_document(request: Request, document: str):
#     doc = {"content": document}
#     return templates.TemplateResponse("index.html", {"request": request, "output": "Document Inserted Successfully"})

# @app.get("/get", response_class=HTMLResponse)
# async def get_best_document(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})

# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=9567)
from fastapi import FastAPI, Request, Form, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from elasticsearch import Elasticsearch
import uvicorn

app = FastAPI()
es = Elasticsearch("http://localhost:9200")
templates = Jinja2Templates(directory="templates")

INDEX_NAME = "words"

if not es.indices.exists(index=INDEX_NAME):
    es.indices.create(index=INDEX_NAME, body={
        "mappings": {
            "properties": {
                "line_number": {"type": "integer"},
                "text": {"type": "text"}
            }
        }
    })

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/insert/")
async def insert_text(text: str = Form(...)):
    """Insert text line-by-line into Elasticsearch"""
    lines = text.split("\n")
    for i, line in enumerate(lines, start=1):
        doc = {"line_number": i, "text": line}
        es.index(index=INDEX_NAME, body=doc)
    return {"status": "Inserted successfully"}

@app.get("/get/")
async def get_matching_lines(word: str = Query(..., description="Word to search for")):
    """Search for the word and return lines containing it"""
    query = {
        "query": {
            "match": {"text": word}
        }
    }
    response = es.search(index=INDEX_NAME, body=query)

    matched_lines = [
        {"line_number": hit["_source"]["line_number"], "text": hit["_source"]["text"]}
        for hit in response["hits"]["hits"]
    ]

    return JSONResponse(content={"matched_lines": matched_lines})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9567)
