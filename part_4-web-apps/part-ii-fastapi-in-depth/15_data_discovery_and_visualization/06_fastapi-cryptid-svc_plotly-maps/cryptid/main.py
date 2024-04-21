"""Entrypoint file for FastAPI Cryptid webapp"""

import os

import plotly.express as px
from fastapi import FastAPI, Response

from cryptid.web import creature, explorer, user

app = FastAPI()
app.include_router(explorer.router)
app.include_router(creature.router)
app.include_router(user.router)


@app.get("/test")
def test():
    df = px.data.iris()
    fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species")
    fig_bytes = fig.to_image(format="png")
    return Response(content=fig_bytes, media_type="image/png")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True, port=int(os.getenv("PORT", "8080")))
