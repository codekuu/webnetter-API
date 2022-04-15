#!/usr/bin/python3
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
from routers import webnetter


app = FastAPI(
    title="Webnetter API",
    description="Plug and Play Network Management API built on Docker, fastAPI & Netmiko.",
    version="2.2",
    redoc_url=None,
)

app.mount("/static", StaticFiles(directory="dist/static"), name="static")

app.include_router(webnetter.router, prefix="/webnetter", tags=["webnetter"])


@app.get("/")
@app.get("/{path}")
async def send_frontend():
    return FileResponse("./dist/index.html")
