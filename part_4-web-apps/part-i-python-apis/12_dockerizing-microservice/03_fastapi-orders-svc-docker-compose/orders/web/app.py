"""FastAPI app entrypoint"""
import os
from pathlib import Path

import yaml
from fastapi import FastAPI
from jwt import (
    ExpiredSignatureError,
    ImmatureSignatureError,
    InvalidAlgorithmError,
    InvalidAudienceError,
    InvalidKeyError,
    InvalidSignatureError,
    InvalidTokenError,
    MissingRequiredClaimError,
)
from starlette import status
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from orders.web.api.auth import decode_and_validate_token

app = FastAPI(
    debug=True, openapi_url="/openapi/orders.json", docs_url="/docs/orders"
)

app.openapi = lambda: oas_doc
oas_doc = yaml.safe_load((Path(__file__).parent / "../../oas.yaml").read_text())


class AuthorizeRequestMiddleware(BaseHTTPMiddleware):
    """Starlette middleware that performs auth check on protected endpoints"""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        # Check feature flag that disables auth (for testing purposes)
        if os.getenv("AUTH_ON", "False").lower() != "True".lower():
            request.state.user_id = "test"
            return await call_next(request)

        # Check if requesting public endpoint
        if request.url.path in ["/docs/orders", "/openapi/orders.json"]:
            return await call_next(request)

        # Check if OPTIONS
        if request.method == "OPTIONS":
            return await call_next(request)

        # Otherwise: process request
        bearer_token = request.headers.get("Authorization")
        if not bearer_token:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "detail": "Missing access token",
                    "body": "Missing access token",
                },
            )

        if not bearer_token.startswith("Bearer "):
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "detail": "Unexpected authorization format",
                    "body": "Unexpected authorization format",
                },
            )

        try:
            auth_token = bearer_token.split(" ")[1].strip()
            token_payload = decode_and_validate_token(auth_token)
        except (
            ExpiredSignatureError,
            ImmatureSignatureError,
            InvalidAlgorithmError,
            InvalidAudienceError,
            InvalidKeyError,
            InvalidSignatureError,
            InvalidTokenError,
            MissingRequiredClaimError,
        ) as error:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": str(error), "body": str(error)},
            )
        else:
            request.state.user_id = token_payload["sub"]
        return await call_next(request)


app.add_middleware(AuthorizeRequestMiddleware)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from orders.web.api import api
