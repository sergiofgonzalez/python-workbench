"""A hello, world! FastAPI app using async"""
import asyncio

from fastapi import FastAPI

app = FastAPI()


@app.get("/hi")
async def greet():
    await asyncio.sleep(3)  # simulates 3 sec delay to retrieve message from db
    return "Hello, async FastAPI!"
