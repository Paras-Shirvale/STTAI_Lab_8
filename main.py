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

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from elasticsearch import Elasticsearch
import uvicorn

app = FastAPI()
es = Elasticsearch("http://localhost:9200")  # Connect to Elasticsearch
templates = Jinja2Templates(directory="templates")

INDEX_NAME = "documents"

# Ensure the index exists
if not es.indices.exists(index=INDEX_NAME):
    es.indices.create(index=INDEX_NAME)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/insert/")
async def insert_word(word: str):
    doc = {"word": word}
    res = es.index(index=INDEX_NAME, body=doc)
    return {"inserted": res['result']}


@app.get("/get")
async def get_best_document(paragraph: str):
    words = paragraph.lower().split()  # Tokenize paragraph
    matched_words = {}

    for word in words:
        query = {
            "query": {
                "match": {"content": word}  # Search for each word
            }
        }
        response = es.search(index=INDEX_NAME, body=query)

        if response["hits"]["total"]["value"] > 0:
            matched_words[word] = [hit["_source"]["content"] for hit in response["hits"]["hits"]]

    return JSONResponse(content={"matched_words": matched_words})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9567)



import requests

response = requests.get("http://localhost:9200/words/_search?pretty")
print(response.text)  # Print response as text
