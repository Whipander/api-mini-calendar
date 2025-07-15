import json
from urllib.request import Request

from fastapi import FastAPI, requests
from starlette.responses import Response, JSONResponse

app = FastAPI()


@app.get("/")
def root(request: requests.Request):
    accept_header = request.headers.get("Accept")
    if accept_header != "text/html" and accept_header != "text/plain":
        return JSONResponse(content={
            "message": """Le type de format attendu n'est pas supporté. Seul les types '`text/html' et 'text/plain' sont supportés."""},
                            status_code=400)
    with open("welcome.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    return Response(content=html_content, status_code=200, media_type="text/html")


@app.get("/{full_path:path}")
def catch_all(full_path: str):
    not_found_message = {"detail": f"Page '/{full_path}' not found"}
    return Response(content=json.dumps(not_found_message), status_code=404, media_type="application/json")
