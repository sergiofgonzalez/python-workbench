import uuid
from datetime import datetime

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class TagIn(BaseModel):
    tag: str


class Tag(BaseModel):
    id: str
    tag: str
    created: datetime


class TagOut(BaseModel):
    tag: str
    created: datetime


tags: dict[str, Tag] = dict()


@app.post("/", status_code=201)
def create(tag_in: TagIn) -> TagIn:
    tag: Tag = Tag(
        id=str(str(uuid.uuid4())), tag=tag_in.tag, created=datetime.utcnow()
    )
    tags[tag.tag] = tag
    return tag_in


@app.get("/{tag_str}", response_model=TagOut)
def get_one(tag_str: str) -> TagOut:
    if tag_str in tags:
        tag = tags[tag_str]
        return tag  # type: ignore
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Tag {tag_str!r} was not found",
        )
