from enum import Enum
import datetime
import uuid
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List

app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]

def generate_random_uuid4() -> int:
    return int(uuid.uuid4())

@app.get('/')
def root() -> JSONResponse:
    return JSONResponse(content="Hello, welcome to this service!")

@app.post("/post")
def get_post() -> Timestamp:
    item_id = generate_random_uuid4()
    time_now = int(datetime.datetime.now().timestamp())
    ts_object = Timestamp(id=item_id, timestamp=time_now)

    post_db.append(ts_object)

    return ts_object

@app.get("/dog")
def get_dog(god_type: DogType) -> List:
    dogs_list = list(dogs_db.values())
    selected_dogs = []

    for dog in dogs_list:
        if dog.kind == god_type:
            selected_dogs.append(dog)
    
    return selected_dogs

@app.get("/dog/{pk}")
def get_dog_by_pk(pk: int) -> Dog:
    dog = dogs_db.get(pk)
    if not dog:
        raise ValueError(f"Dog with {pk} does not exist!")

    return dog

@app.post("/dog")
def add_new_dog(dog: Dog) -> Dog:
    if dog.pk not in dogs_db:
        dogs_db[dog.pk] = dog
    else:
        raise ValueError(f"Dog with {dog.pk} already exists!")

    return dog

@app.patch("/dog/{pk}")
def dog_update(pk: int, dog: Dog) -> Dog:
    if dog.pk != pk:
        raise ValueError(f"Trying to change dog with id {pk}, but Dog passed with another id {dog.pk}")
    else:
        dogs_db[pk] = dog
    
    return dog
