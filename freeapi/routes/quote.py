import json
from typing import Any

import aiofile
from fastapi import APIRouter, Depends, HTTPException, Query

from freeapi.constants import JSON_DIR_PATH
from freeapi.models.quote import Quote
from freeapi.utils.helper import get_paginated_payload, get_randint

QUOTES_JSON_PATH = JSON_DIR_PATH / "quotes.json"

router = APIRouter()


async def read_quotes() -> list[dict[str, Any]]:
    async with aiofile.async_open(QUOTES_JSON_PATH) as f:
        quotes = await f.read()
    return json.loads(quotes)


@router.get(
    "/random",
    response_model=Quote,
    description="Get a random quote on every request.",
)
async def get_random_quote(
    quotes: list[dict[str, Any]] = Depends(read_quotes),
):
    randint = get_randint(0, len(quotes) - 1)
    return quotes[randint]


@router.get(
    "/id/{quote_id}",
    response_model=Quote,
    description="Get quote of specified id.",
)
async def get_quote_by_id(
    quote_id: int,
    quotes: list[dict[str, Any]] = Depends(read_quotes),
):
    for quote in quotes:
        if quote["id"] == quote_id:
            return quote
    raise HTTPException(400, f"{quote_id=} not exists.")


@router.get("/")
async def get_quotes(
    query: str = Query("human"),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=30),
    quotes: list[dict[str, Any]] = Depends(read_quotes),
):
    payload = [quote for quote in quotes if query.lower() in quote["content"].lower()]
    return get_paginated_payload(payload, page, limit)


@router.get(
    "/authors",
    description=(
        "Get all distinct authors' slug and name. Also get how many quotes were "
        "written by the author."
    ),
)
async def get_authors_detail(
    quotes: list[dict[str, Any]] = Depends(read_quotes),
):
    authors_detail = {}
    for quote in quotes:
        author_slug = quote.get("authorSlug")
        author_name = quote.get("author")
        if author_slug not in authors_detail:
            authors_detail[author_slug] = {"name": author_name, "quoteCount": 0}
        authors_detail[author_slug]["quoteCount"] += 1
    return {
        "totalAuthors": len(authors_detail),
        "authorsDetail": authors_detail,
    }


@router.get(
    "/author/{author_slug}",
    response_model=list[Quote],
    description="Get quotes of specified author.",
)
async def get_quotes_by_author(
    author_slug: str,
    quotes: list[dict[str, Any]] = Depends(read_quotes),
):
    payload = [quote for quote in quotes if quote["authorSlug"] == author_slug]
    if not payload:
        raise HTTPException(400, f"{author_slug=} not exists.")
    return payload


@router.get(
    "/tags",
    description="Get all distinct tags. Also get how many quotes were tagged with it",
)
async def get_tags_detail(
    quotes: list[dict[str, Any]] = Depends(read_quotes),
):
    tags_detail = {}
    for tag in [tag for quote in quotes for tag in quote["tags"]]:
        if tag not in tags_detail:
            tags_detail[tag] = {"quoteCount": 1}
        else:
            tags_detail[tag]["quoteCount"] += 1
    return {
        "totaltags": len(tags_detail),
        "tagsDetail": tags_detail,
    }


@router.get(
    "/tag/{tag}",
    response_model=list[Quote],
    description="Get quotes of specified tag.",
)
async def get_quotes_by_tag(
    tag: str,
    only: bool = True,
    quotes: list[dict[str, Any]] = Depends(read_quotes),
):
    if not tag:
        raise HTTPException(400, "Query `tag` must not be empty.")

    tags = tag.lower().split(",")
    if only and len(tags) > 1:
        raise HTTPException(
            400,
            "Provide only one tag or specify `only` query as `false`.",
        )

    return [
        quote
        for quote in quotes
        if any(t in map(str.lower, quote["tags"]) for t in tags)
    ]
