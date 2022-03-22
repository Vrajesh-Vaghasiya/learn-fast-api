import time
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
    time.sleep(5)
    return {"message": "Hello world!!"}


def delay():
    time.sleep(5)
    return {"message": "Wow!!"}


@university.get("/item/{item_id}")
def read_items(item_id: int, q:Optional[str] = None):
    del_res = delay()
    return {"item_id": item_id, "q": q, "delay_response": del_res.get("message") if del_res else None}


# Declare models
class Item(BaseModel):
    name: str
    price: int
    description: Optional[str] = None


@university.post("/item/")
def create_item(item: Item):
    return item

@university.get('/items/')
def read_items(q: Optional[List[str]] = Query(['test_item1', 'test_item2'])):
    query_items = {"q": q}
    return query_items



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