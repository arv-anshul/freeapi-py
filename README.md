# freeapi-py

<p align="center">
  <img src="https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=fff&style=flat" alt="Docker Badge">
  <img src="https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=fff&style=flat" alt="FastAPI Badge">
  <img src="https://img.shields.io/badge/MongoDB-47A248?logo=mongodb&logoColor=fff&style=flat" alt="MongoDB Badge">
  <img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff&style=flat" alt="Python Badge">
  <img src="https://img.shields.io/badge/Rye-000?logo=rye&logoColor=fff&style=flat" alt="Rye Badge">
  <img src="https://img.shields.io/badge/UV-D7FF64?logo=ruff&logoColor=000&style=flat" alt="UV Badge">
</p>

A knack to create similar APIs present in [freeapi.app] project using Python, FastAPI and MongoDB.
I've used Docker so that anyone can easily reproduce this project in their system.

## Setup Docker Container

Clone the repo.

```bash
git clone https://github.com/arv-anshul/freeapi-py
```

Use `docker compose` to build and run the container.

I've used [`uv`][uv] to install packages in the docker container this reduces the build time significantly.

```bash
docker compose up --build  # For the first time
```

## Roadmap

- [x] Use [`rye`][rye] for local package management tool.
- [x] Create Todo APIs.
- [x] Containerise the FastAPI app with Docker.
- [x] Use [`uv`][uv] in container for package installation.
- [x] Add `/quote` routes.

[freeapi.app]: https://freeapi.app
[rye]: https://rye-up.com
[uv]: https://astral.sh/uv
