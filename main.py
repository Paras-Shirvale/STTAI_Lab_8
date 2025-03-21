from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()

# Define the templates directory
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/insert", response_class=HTMLResponse)
async def insert_document(request: Request, document: str):
    doc = {"content": document}
    return templates.TemplateResponse("index.html", {"request": request, "output": "Document Inserted Successfully"})

@app.get("/get", response_class=HTMLResponse)
async def get_best_document(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9567)
