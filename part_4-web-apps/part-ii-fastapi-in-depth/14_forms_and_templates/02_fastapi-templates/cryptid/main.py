"""Entrypoint file for FastAPI Cryptid webapp"""

import os
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from cryptid.web import creature, explorer, user

app = FastAPI()
app.include_router(explorer.router)
app.include_router(creature.router)
app.include_router(user.router)

BASE_DIR = Path(__file__).resolve().parent

template_obj = Jinja2Templates(directory=BASE_DIR / "template")


@app.get("/")
def home(request: Request):
    explorers = explorer.get_all()
    return template_obj.TemplateResponse(
        "list.html",
        {
            "request": request,
            "explorers": explorers,
            "creatures": creature.get_all(),
        },
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True, port=int(os.getenv("PORT", "8080")))
