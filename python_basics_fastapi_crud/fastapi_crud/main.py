from fastapi import FastAPI, HTTPException
from model import Item
from services import (
    create_item,
    get_items,
    get_item,
    update_item,
    delete_item
)

app = FastAPI()

@app.post("/items/")
def create(item: Item):
    try:
        return create_item(item)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/items/")
def all_items():
    return get_items()

@app.get("/items/{item_id}")
def read(item_id: int):
    item = get_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put("/items/{iten_id}")
def update(item_id: int, item: Item):
    return update_item(item_id, item)

@app.delete("/items/{iten_id}")
def delete(item_id: int):
    result = delete_item(item_id)
    if not result:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Deleted"}
    

