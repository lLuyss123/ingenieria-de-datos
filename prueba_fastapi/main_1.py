from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    id:int
    name:str

class UserUpdate(BaseModel):
    name: str

users= []

@app.get("/users")
def get_users():
    return users

@app.post("/users")
def create_user(user:User):
    users.append(user)
    return user

@app.put("/users/{id}")
def update_user(id: int, user: UserUpdate):
    for eachuser in users:
        if eachuser["id"] == id:
            eachuser.update(user)
            return eachuser

    return {"error": "Usuario no encontrado"}


@app.delete("/users/{id}")
def delete_user(id: int):
    for user in users:
        if user["id"] == id:
            users.remove(user)
            return {"message": "Usuario eliminado correctamente"}

    return {"error": "Usuario no encontrado"}
