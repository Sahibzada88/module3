from fastapi import FastAPI, Body
from menu_data import menu

app = FastAPI()

@app.get("/")
def get_menu():
    return {"Menu": menu}

@app.post("/menu/")
def add_menu_item(new_item: dict = Body(...)):
    if any(item["id"] == new_item["id"] for item in menu):
        return {"error": "Menu item with this ID already exists"}, 400
    
    menu.append(new_item)
    return {"message": "Menu item added successfully", "menu": menu}

@app.put("/menu/{item_id}")
def update_menu_item(item_id: int, item_data: dict = Body(...)):
    # Find the menu item by its ID
    item = next((m for m in menu if m["id"] == item_id), None)
    if item:
        # Update the item with the new data
        item.update(item_data)
        return {"message": "Menu item updated successfully", "menu_item": item}
    return {"error": "Menu item not found", "menu": menu}, 404

@app.delete("/menu/{menu_id}")
def delete_menu(menu_id: int):
    global menu
    menu = [m for m in menu if m["id"] != menu_id]
    return {"message": "menu deleted", "menu": menu}, 200


