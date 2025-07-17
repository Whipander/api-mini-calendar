import json
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import Response, JSONResponse
from starlette.requests import Request
from typing import List

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
        return JSONResponse(content={"message": f"""La clé API fournie: {x_api_key} ; n'est pas reconnue."""})


class EventModel(BaseModel):
    name: str
    description: str
    start_date: str
    end_date: str


events_store: List[EventModel] = []


def serialized_stored_events():
    events_converted = []
    for event in events_store:
        events_converted.append(event.model_dump())
    return events_converted


@app.get("/events")
def list_events():
    return {"events": serialized_stored_events()}


@app.post("/events")
def create_event(events: List[EventModel]):
    for event in events:
        events_store.append(event)
    return {"events": serialized_stored_events()}


@app.put("/events")
def update_event(events: List[EventModel]):
    for eventUpdated in events:
        found = False
        for index, oldEvent in enumerate(events_store):
            if oldEvent.name == eventUpdated.name:
                events_store[index] = eventUpdated
                found = True
                break
        if not found:
            events_store.append(eventUpdated)
    return {"events": serialized_stored_events()}


# 404 handling
@app.get("/{full_path:path}")
def catch_all():
    with open("404.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    return Response(content=html_content, status_code=404, media_type="text/html")
