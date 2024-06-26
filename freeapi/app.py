import sys

from fastapi import FastAPI

from freeapi import middleware
from freeapi.routes import fun, gh, quote, todo

app = FastAPI(
    title="FreeAPI",
    description="Recreation of freeapi.app project in python using FastAPI.",
    docs_url="/",
)

app.middleware("process_time")(middleware.add_process_time_header)


@app.get("/root")
def root():
    return {
        "message": "Namaste!",
        "pyVersion": sys.version,
    }


app.include_router(
    todo.router,
    prefix="/todo",
    tags=["todo"],
)
app.include_router(
    quote.router,
    prefix="/quote",
    tags=["quote"],
)
app.include_router(
    gh.router,
    prefix="/gh",
    tags=["github"],
)
app.include_router(
    fun.router,
    prefix="/fun",
    tags=["fun"],
)
