from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn  
import requests
import logging

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://{External_ip_fronend_container}:9567"],          # Add the external IP of the frontend container
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FastAPI Frontend</title>
    <script>
        async function sendRequest(route, params, method="GET") {
            const url = new URL("http://localhost:8080" + route);
            Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));
            const options = { method };
            let response = await fetch(url, options);
            let data = await response.json();
            document.getElementById("output").innerText = data.message || "Result: " + (data.result || "Not found");
        }

        function insertData() {
            sendRequest("/insert", { key: document.getElementById("key").value, value: document.getElementById("value").value }, "POST");
        }

        function searchData() {
            sendRequest("/search", { key: document.getElementById("key").value });
        }
    </script>
</head>
<body>
    <h1>FastAPI Frontend</h1>
    <label>Key:</label>
    <input type="text" id="key">
    <label>Value:</label>
    <input type="text" id="value">
    <button onclick="insertData()">Insert</button>
    <button onclick="searchData()">Search</button>
    <p id="output"></p>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    return HTMLResponse(content=HTML_CONTENT)

# insert endpoint
@app.post("/insert")
async def insert_doc(request: Request):
    data = await request.json()
    responses = requests.post("http://{External_ip_fronend_container}:9567" + "/insert", json = data).json()
    logger.info("Inserting to db...")
    return responses

# search endpoint
@app.get("/search")
async def search_(query):
    return requests.get("http://{External_ip_fronend_container}:9567" + "/search", params = {"query": query}).json()

if __name__ == "__main__":
    uvicorn.run(app, host = "0.0.0.0", port = 9567)