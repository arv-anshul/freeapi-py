"""
In this router I've used below listed api endpoints:

Uses GitHub APIs:
- https://api.github.com/users/arv-anshul
- https://api.github.com/repos/arv-anshul/freeapi-py
- https://api.github.com/repos/arv-anshul/freeapi-py/community/profile
- https://api.github.com/repos/arv-anshul/freeapi-py/traffic/views  # requires API_TOKEN
- https://api.github.com/repos/arv-anshul/freeapi-py/traffic/clones  # requires API_TOKEN
"""

import asyncio

from fastapi import APIRouter
from pydantic import BaseModel

from freeapi.models.gh import GHRepo, GHRepoCommunity, GHUser
from freeapi.utils.helper import request

router = APIRouter()

BASE_GH_API = "https://api.github.com"


@router.get(
    "/user/{username}",
    response_model=GHUser,
)
async def get_user_info(
    username: str,
):
    """
    This endpoint will gives you details about GitHub account/user.

    Uses GitHub APIs:
    - https://api.github.com/users/{username}
    """
    response = await request("GET", f"{BASE_GH_API}/users/{username}")
    return GHUser.model_validate_json(response)


class _GHRepoInfo(BaseModel):
    """Created just for endpoint responses."""

    repoInfo: GHRepo
    repoCommunityDetails: GHRepoCommunity


@router.get(
    "/repo/{username}/{repo}",
    response_model=_GHRepoInfo,
)
async def get_repo_info(
    username: str,
    repo: str,
):
    """
    This endpoint will gives you details about GitHub repo.

    Uses GitHub APIs:
    - https://api.github.com/repos/{username}/{repo}
    - https://api.github.com/repos/{username}/{repo}/community/profile
    """
    repo_info, community_details = await asyncio.gather(
        request("GET", f"{BASE_GH_API}/repos/{username}/{repo}"),
        request("GET", f"{BASE_GH_API}/repos/{username}/{repo}/community/profile"),
    )
    return {
        "repoInfo": GHRepo.model_validate_json(repo_info),
        "repoCommunityDetails": GHRepoCommunity.model_validate_json(community_details),
    }
