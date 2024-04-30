from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Query
from motor.motor_asyncio import AsyncIOMotorCollection

from ..models.todo import Todo, TodoInDB, TodoStatus, UpdateTodo
from ..mongo import get_mongo_client, validate_objectid

router = APIRouter()


def get_todo_collection() -> AsyncIOMotorCollection:
    client = get_mongo_client()
    return client["todo"]


@router.get(
    "/{todo_id}",
    response_model=TodoInDB,
    description="Get specific todo by providing its id.",
)
async def get_todo(
    todo_id: str,
    collection: AsyncIOMotorCollection = Depends(get_todo_collection),
):
    result = await collection.find_one({"_id": ObjectId(todo_id)})
    if result:
        return result
    raise HTTPException(400, f"todo_id={todo_id!r} not found.")


@router.get(
    "/",
    response_model=list[TodoInDB],
    description="Get a list of todos from database.",
)
async def get_many_todo(
    limit: int = Query(10, ge=1, le=50),
    status: TodoStatus | None = None,
    collection: AsyncIOMotorCollection = Depends(get_todo_collection),
):
    # TODO: Return random todo on every request
    filter_ = {}
    if status:
        filter_["status"] = status

    result = await collection.find(filter_).to_list(limit)
    if len(result) == limit:
        return result
    raise HTTPException(400, "Length of result todo < limit")


@router.post(
    "/",
    status_code=201,
    description="Create a new todo item by providing the title and description.",
)
async def create_todo(
    todo: Todo,
    collection: AsyncIOMotorCollection = Depends(get_todo_collection),
):
    result = await collection.insert_one(todo.model_dump())
    return TodoInDB(_id=result.inserted_id, **todo.model_dump())


@router.patch(
    "/{todo_id}",
    status_code=200,
    description="Update todo's title and description.",
)
async def update_todo(
    todo_id: str,
    todo: UpdateTodo,
    collection: AsyncIOMotorCollection = Depends(get_todo_collection),
):
    validate_objectid(todo_id)
    result = await collection.update_one(
        {"_id": ObjectId(todo_id)},
        {"$set": todo.model_dump(exclude_defaults=True)},
    )
    if result.matched_count == 0:
        raise HTTPException(400, f"0 todo matches with id={todo_id}")
    if result.modified_count == 1:
        return {"message": f"Updated todo with id={todo_id}"}
    raise HTTPException(400, "Todo not found.")


@router.patch(
    "/{status}/{todo_id}",
    status_code=200,
    description="This endpoint will update todo status.",
)
async def update_todo_status(
    status: TodoStatus,
    todo_id: str,
    collection: AsyncIOMotorCollection = Depends(get_todo_collection),
):
    validate_objectid(todo_id)
    result = await collection.update_one(
        {"_id": ObjectId(todo_id)},
        {"$set": {"status": status}},
    )
    if result.modified_count == 1:
        return {"message": f"Toggled todo status with id={todo_id}"}
    raise HTTPException(400, "Todo not found.")


@router.delete(
    "/{todo_id}",
    status_code=200,
    description="Delete todo from database by specifying its id.",
)
async def delete_todo(
    todo_id: str,
    collection: AsyncIOMotorCollection = Depends(get_todo_collection),
):
    validate_objectid(todo_id, "Invalid todo_id")
    result = await collection.delete_one({"_id": ObjectId(todo_id)})
    if result.deleted_count == 1:
        return {"message": f"Deleted todo with id={todo_id}"}
    raise HTTPException(400, "Todo not found")
