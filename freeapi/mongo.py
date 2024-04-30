from __future__ import annotations

import os

from bson import ObjectId
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


def get_mongo_client() -> AsyncIOMotorDatabase:
    client = AsyncIOMotorClient(os.getenv("MONGODB_URL"))
    return client["freeapi"]


def validate_objectid(
    id_: str | ObjectId,
    msg: str | None = None,
):
    """
    Validate `ObjectId` with `ObjectId.is_valid` method.

    Args:
        id_ (str | ObjectId): ObjectId to validate.
        msg (str | None): Custom error message. If `None`, `msg="Invalid id"`.

    Raises `fastapi.HTTPException` with `400` status code.
    """
    if not ObjectId.is_valid(id_):
        if not msg:
            msg = "Invalid id"
        raise HTTPException(400, msg)
