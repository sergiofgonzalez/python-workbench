"""Entrypoint file for FastAPI Cryptid webapp"""

import os

from fastapi import FastAPI

from cryptid.web import creature, explorer, user

app = FastAPI()
app.include_router(explorer.router)
app.include_router(creature.router)
app.include_router(user.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True, port=int(os.getenv("PORT", "8080")))
