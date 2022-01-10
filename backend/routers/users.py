from typing import List

from pydantic import parse_obj_as
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db import schemas, crud, models
from dependencies import get_db, manager

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[schemas.User], dependencies=[Depends(manager)])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/me", response_model=schemas.User)
def read_current_user(user: models.User = Depends(manager)):
    return schemas.User.from_orm(user)


@router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/{user_id}/{animal_id}", response_model=schemas.Animal)
def add_animal_to_user(user_id: int, animal_id: int, db: Session = Depends(get_db)):
    return crud.add_animal_to_user(db, user_id=user_id, animal_id=animal_id)


@router.get("/animals/{user_id}", response_model=List[schemas.Animal])
def read_all_animals_by_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_all_animal_by_user(db, user_id=user_id)
