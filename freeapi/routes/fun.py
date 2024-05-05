import json

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import RedirectResponse

from freeapi.utils.helper import request

router = APIRouter()


async def get_emojis_as_dict():
    """
    FIXME: This function calls every times whenever you hit request to dependent
    endpoints even if `use_cache` argument in `Depends` function is set to true.
    Due to this the dependent endpoints are slow.
    """
    res = await request("GET", "https://api.github.com/emojis")
    return json.loads(res)


@router.get(
    "/emojis",
    status_code=307,
    tags=["emoji"],
)
async def redirect_to_github_emojis_api():
    return RedirectResponse("https://api.github.com/emojis")


@router.get(
    "/emoji/url",
    response_model=dict,
    tags=["emoji"],
)
async def get_emoji_as_url(
    name: str,
    emojis: dict[str, str] = Depends(get_emojis_as_dict),
):
    """
    Get the queried emoji.

    Uses GitHub's API:
    - https://api.github.com/emojis
    """
    emoji_url = emojis.get(name)
    if not emoji_url:
        raise HTTPException(400, f"{name=} is not a valid emoji name.")
    return {
        "name": name,
        "url": emoji_url,
    }


@router.get(
    "/emoji/png",
    tags=["emoji"],
)
async def get_emoji_as_png(
    name: str,
    emojis: dict[str, str] = Depends(get_emojis_as_dict),
):
    """
    Get emoji in PNG response.

    You can also use `/emoji/png/redirect` endpoint which is more efficient than this
    endpoint.
    """
    emoji_url = emojis.get(name)
    if not emoji_url:
        raise HTTPException(400, f"{name=} is not a valid emoji name.")
    emoji_bytes = await request("GET", emoji_url)
    return Response(emoji_bytes, media_type="image/png")


@router.get(
    "/emoji/png/redirect",
    tags=["emoji"],
)
async def redirect_for_emoji_as_png(
    name: str,
    emojis: dict[str, str] = Depends(get_emojis_as_dict),
):
    """
    Redirects to emoji's png url.

    Uses GitHub's API:
    - https://api.github.com/emojis
    """
    emoji_url = emojis.get(name)
    if not emoji_url:
        raise HTTPException(400, f"{name=} is not a valid emoji name.")
    return RedirectResponse(emoji_url)
