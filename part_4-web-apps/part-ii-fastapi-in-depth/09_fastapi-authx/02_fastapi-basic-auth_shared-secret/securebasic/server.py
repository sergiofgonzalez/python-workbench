"""FastAPI web app with HTTP Basic Auth"""

from datetime import datetime

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()

basic = HTTPBasic()

secret_user: str = "bill.harford"
secret_pass: str = "fidelio"


@app.get("/who")
def get_user_credentials(creds: HTTPBasicCredentials = Depends(basic)) -> dict:
    if creds.username == secret_user and creds.password == secret_pass:
        return {"username": creds.username, "password": creds.password}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrent user or password",
    )


@app.get("/health-check")
def health_check():
    return {"now": datetime.utcnow(), "status": "OK"}


if __name__ == "__main__":
    uvicorn.run("securebasic.server:app", port=8080, reload=True)
