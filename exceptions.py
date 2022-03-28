from main import university, Item, items
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

# update data
@university.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found", headers={"X-Error": "There   goes my error"}, )
    else:
        return items[item_id]


@university.patch("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: Item):
    update_item_encoded = jsonable_encoder(item)
    items[item_id] = update_item_encoded
    return update_item_encoded

# make crud for items