import sys

from fastapi import FastAPI

from freeapi import middleware
from freeapi.routes import todo

app = FastAPI(
    title="FreeAPI",
    description="Recreation of freeapi.app project in python using FastAPI.",
)

app.middleware("process_time")(middleware.add_process_time_header)


@app.get("/")
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
