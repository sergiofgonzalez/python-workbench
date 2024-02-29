"""FastAPI web app with HTTP Basic Auth"""

from datetime import datetime

import uvicorn
from fastapi import Depends, FastAPI
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()

basic = HTTPBasic()


@app.get("/who")
def get_user_credentials(creds: HTTPBasicCredentials = Depends(basic)):
    return {"username": creds.username, "password": creds.password}


@app.get("/health-check", dependencies=[Depends(basic)])
def health_check():
    return {"now": datetime.utcnow(), "status": "OK"}


@app.get("/")
def top_public():
    return {"endpoints": ["/", "/who", "/health-check"]}


if __name__ == "__main__":
    uvicorn.run("securebasic.server:app", port=8080, reload=True)
