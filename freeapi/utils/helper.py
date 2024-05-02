import secrets
from typing import Any, Literal

import httpx
from fastapi import HTTPException


def get_randint(low: int, high: int, /) -> int:
    return low + secrets.randbelow(high - low)


def get_paginated_payload(data: list[Any], page: int, limit: int):
    start_position = (page - 1) * limit

    total_items = len(data)
    total_pages = -(-total_items // limit)

    filtered_data = data[start_position : start_position + limit]
    return {
        "current_page_items": len(filtered_data),
        "data": filtered_data,
        "limit": limit,
        "next_page": page < total_pages,
        "page": page,
        "previous_page": page > 1,
        "total_items": total_items,
        "total_pages": total_pages,
    }


async def request(
    method: Literal["GET", "POST"],
    url: str,
    /,
    json: Any = None,
) -> bytes:
    r = httpx.request(method, url, json=json)
    if r.status_code != 200:
        raise HTTPException(
            400,
            {
                "message": "Error while making project.",
                "method": method,
                "url": url,
                "status_code": r.status_code,
            },
        )
    return r.content
