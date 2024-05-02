from typing import Any

from pydantic import BaseModel, Field


class GHUser(BaseModel):
    avatar_url: str
    bio: str
    blog: str
    company: Any
    created_at: str
    email: Any
    followers: int
    following: int
    gravatar_id: str
    hireable: Any
    html_url: str
    id: int
    location: str
    login: str
    name: str
    public_gists: int
    public_repos: int
    twitter_username: Any


class GHRepoOwner(BaseModel):
    login: str
    id: int
    avatar_url: str


class GHLicense(BaseModel):
    key: str
    name: str
    spdx_id: str
    url: str | None


class GHRepo(BaseModel):
    id: int
    name: str
    full_name: str
    private: bool
    owner: GHRepoOwner
    html_url: str
    description: str
    fork: bool
    created_at: str
    homepage: str
    size: int
    stargazers_count: int
    watchers_count: int
    language: str
    has_issues: bool
    has_projects: bool
    has_downloads: bool
    has_wiki: bool
    has_pages: bool
    has_discussions: bool
    forks_count: int
    archived: bool
    disabled: bool
    open_issues_count: int
    license: GHLicense
    allow_forking: bool
    is_template: bool
    topics: list[str]
    visibility: str
    default_branch: str
    network_count: int
    subscribers_count: int


class GHRepoDetails(BaseModel):
    code_of_conduct: Any
    code_of_conduct_file: Any
    contributing: Any
    issue_template: Any
    pull_request_template: Any
    readme: Any


class GHRepoCommunity(BaseModel):
    health_percentage: int
    documentation: Any
    details: GHRepoDetails = Field(alias="files", serialization_alias="details")
