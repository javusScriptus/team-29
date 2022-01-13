from db.database import engine
from sqlalchemy.orm import Session
from . import models, schemas
from dependencies import manager, get_db
from fastapi import Depends

from .schemas import Role


@manager.user_loader()
def loader(username: str):
    user: models.User
    with Session(engine) as db:
        user = db.query(models.User).filter(models.User.username == username).first()
    return user


def get_user_by_username(username: str, db: Session):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user(user_id: int, db: Session) -> models.User:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(email: str, db: Session):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100, exclude_admin: bool = False):
    if exclude_admin:
        return db.query(models.User) \
            .filter(models.User.role == Role.USER) \
            .offset(skip) \
            .limit(limit) \
            .all()
    else:
        return db.query(models.User) \
            .offset(skip) \
            .limit(limit) \
            .all()


def create_user(user: schemas.UserCreate, db: Session):
    db_user = models.User(email=user.email, username=user.username, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(user: models.User, new_details: schemas.UserUpdate, db: Session):
    for key, val in new_details.dict(exclude_unset=True).items():
        setattr(user, key, val)
    db.add(user)
    db.commit()
    return user


def create_animal(animal: schemas.AnimalCreate, db: Session):
    db_animal = models.Animal(**animal.dict())
    db.add(db_animal)
    db.commit()
    db.refresh(db_animal)
    return db_animal


def get_animal(animal_id: int, db: Session):
    return db.query(models.Animal).filter(models.Animal.id == animal_id).first()


def get_animals(db: Session):
    return db.query(models.Animal).all()


def add_animal_to_user(user_id: int, animal_id: int, db: Session):
    user = get_user(user_id=user_id, db=db)
    animal = get_animal(animal_id=animal_id, db=db)
    user.animals.append(animal)
    db.commit()
    return animal


def get_all_animal_by_user(user_id: int, db: Session):
    user = get_user(user_id=user_id, db=db)
    return user.animals
