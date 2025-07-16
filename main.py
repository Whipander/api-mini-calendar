import json
from fastapi import FastAPI
from starlette.responses import Response, JSONResponse
from starlette.requests import Request
app = FastAPI()


@app.get("/")
def root(request: Request):
    accept_header = request.headers.get("Accept")
    x_api_key = request.headers.get("x-api-key")

    if accept_header != "text/html" and accept_header != "text/plain":
        return JSONResponse(content={
            "message": """Le type de format attendu n'est pas supporté. Seul les types '`text/html' et 'text/plain' sont supportés."""},
            status_code=400)
    if x_api_key == "12345678":
        with open("welcome.html", "r", encoding="utf-8") as file:
            html_content = file.read()
        return Response(content=html_content, status_code=200, media_type="text/html")
    else:
        return JSONResponse(content={"message" : f"""La clé API fournie: {x_api_key} ; n'est pas reconnue."""})


@app.get("/{full_path:path}")
def catch_all(full_path: str):
    with open("404.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    return Response(content=html_content, status_code=404, media_type="text/html")

