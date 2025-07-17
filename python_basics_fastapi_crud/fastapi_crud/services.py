import json
from pathlib import Path
from model import Item

DATA_FILE = Path("data.json")

# Ensure file exists
if not DATA_FILE.exists():
    DATA_FILE.write_text("{}")

#Reading a file
def read_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)
    
#Writing into a file    
def write_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

#Creating a new item
def create_item(item: Item):
    data = read_data()
    if str(item.id) in data:
        raise ValueError("Item with this ID already exists")
    data[str(item.id)] = item.dict()
    write_data(data)
    return item

#Get all items
def get_items():
    data = read_data()
    return data

#Getting an item
def get_item(item_id: int):
    data = read_data()
    return data.get(str(item_id))

#Updating an existing item
def update_item(item_id: int, item: Item):
    data = read_data()
    if str(item_id) not in data:
        return None
    data[str(item_id)] = item.dict()
    write_data(data)
    return item

#Deleting an existing item
def delete_item(item_id: int):
    data = read_data()
    removed = data.pop(str(item_id), None)
    write_data(data)
    return removed

