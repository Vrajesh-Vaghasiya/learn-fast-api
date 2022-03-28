# import time
from typing import Optional, List
from fastapi import FastAPI, Query
from pydantic import BaseModel, EmailStr
from enum import Enum

university = FastAPI()


# Dropdowns
class DLModels(str, Enum):
    alexnet = "Alexnet"
    resnet = "Resnet"
    lenet = "Lenet"


@university.get("/dl_model/{model_name}")
def get_dl_model(model_name: DLModels):
    if model_name == DLModels.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


@university.get("/")
async def read_root():
    return {"message": "Hello world!!"}


@university.get("/item/{item_id}")
def read_items(item_id: int, q:Optional[str] = None):
    # del_res = delay()
    return {"item_id": item_id, "q": q} #, "delay_response": del_res.get("message") if del_res else None}


# Declare models
class Item(BaseModel):
    name: str
    price: float = 10.2
    description: Optional[str] = None


items = {
    0: {"name": "Foo", "price": 50.2},
    1: {"name": "Bar", "description": "The bartenders", "price": 62},
    2: {"name": "Baz", "description": None, "price": 50.2},
}

@university.post("/item/")
def create_item(item: Item):
    length = len(items)
    items[length+1] = {"name": item.name, "price": item.price, "description": item.description }
    return items[length+1]

@university.get('/items/')
def list_items(q: Optional[List[int]] = Query([0, 1])):
    result = []
    for q_int in q:
        try:
            result.append(items[q_int])
        except:
            pass
    return result



# User code
class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Optional[str] = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None


class UserInDB(BaseModel):
    username: str
    hashed_password: str
    email: EmailStr
    full_name: Optional[str] = None


def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db


@university.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved

# datatype
from datetime import datetime, time, timedelta
from uuid import UUID
from fastapi import Body

@university.put("/items/{item_id}")
async def update_items(
    item_id: UUID,
    start_datetime: Optional[datetime] = Body(None),
    end_datetime: Optional[datetime] = Body(None),
    repeat_at: Optional[time] = Body(None),
    process_after: Optional[timedelta] = Body(None),
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "repeat_at": repeat_at,
        "process_after": process_after,
        "start_process": start_process,
        "duration": duration,
    }


# Forms
from fastapi import Form

@university.post("/login/")
async def login(username: str = Form(...), password: str = Form(...)):
    return {"username": username}


# File upload
from fastapi import File, UploadFile

@university.post("/files/")
async def create_file(file: bytes = File(...)):
    return {"file_size": len(file)}


@university.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}
