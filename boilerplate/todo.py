"""
Add dummy todo data in db using API.
"""

import asyncio
import os

import httpx
from freeapi.models.todo import Todo, TodoStatus

todo_list = (
    Todo(
        status=TodoStatus.DONE,
        title=f"Dummy Todo {i}",
        description=f"Description of Dummy Todo {i}",
    )
    for i in range(40)
)


async def add_dummy_todo_in_db(client: httpx.AsyncClient, todo: Todo) -> None:
    await client.post("/todo/", json=todo.model_dump(mode="json"))


async def main():
    async with httpx.AsyncClient(base_url=os.environ["BASE_API_URL"]) as client:
        await asyncio.gather(
            *(add_dummy_todo_in_db(client, todo) for todo in todo_list),
        )


if __name__ == "__main__":
    asyncio.run(main())
