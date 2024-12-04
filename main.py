from fastapi import FastAPI, Body
from dummy import users

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI REST API!"}

@app.get("/users")
def get_users():
    return {"users": users}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    user = next((u for u in users if u["id"] == user_id), None)
    if user:
        return {"user": user}
    return {"error": "User not found"}, 404

@app.post("/users")
def add_user(user: dict = Body(...)):
    user["id"] = len(users) + 1
    users.append(user)
    return {"user": user}, 201

@app.put("/users/{user_id}")
def update_user(user_id: int, user_data: dict = Body(...)):
    user = next((u for u in users if u["id"] == user_id), None)
    if user:
        user.update(user_data)
        return {"user": user}
    return {"error": "User not found"}, 404

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    global users
    users = [u for u in users if u["id"] != user_id]
    return {"message": "User deleted"}, 200



