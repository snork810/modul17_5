from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from backend.db_depends import get_db
from typing import Annotated
from models.task_model import Task
from models.user_model import User
from schemas import CreateUser, UpdateUser
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter(prefix='/user', tags=['user'])

@router.get('/')
async def all_users(db:Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User).where(User.username != None)).all()
    return users


@router.get('/user_id')
async def user_by_id(db:Annotated[Session, Depends(get_db)], user_id):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User was not found')
    return user

@router.get('/user_id/tasks')
async def tasks_by_user_id(db:Annotated[Session, Depends(get_db)], user_id):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User was not found')
    tasks = db.scalars(select(Task).where(Task.user_id == user_id)).all()
    return tasks

@router.post('/create')
async def create_user(db:Annotated[Session, Depends(get_db)], create_user:CreateUser):
    repete_username = db.scalar(select(User).where(User.username == create_user.username))
    if repete_username is not None:
        raise HTTPException(status_code=status.HTTP_302_FOUND, detail='This username is busy')
    db.execute(insert(User).values(username=create_user.username,
                                   firstname=create_user.firstname,
                                   lastname=create_user.lastname,
                                   age=create_user.age,
                                   slug=slugify(create_user.username)))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}

@router.put('/update')
async def update_user(db:Annotated[Session, Depends(get_db)], user_id, update_user_model:UpdateUser):
    repete_username = db.scalar(select(User).where(User.username == update_user_model.username))
    if repete_username is not None:
        raise HTTPException(status_code=status.HTTP_302_FOUND, detail='This username is busy')
    upd_user = db.scalar(select(User).where(User.id == user_id))
    if upd_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User was not found')
    db.execute(update(User).where(User.id==user_id).values(username=update_user_model.username,
                                                           firstname=update_user_model.firstname,
                                                           lastname=update_user_model.lastname,
                                                           age=update_user_model.age,
                                                           slug=slugify(update_user_model.username)))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User update is successful!'}


@router.delete('/delete')
async def delete_user(db:Annotated[Session, Depends(get_db)], user_id):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User was not found')
    db.execute(delete(Task).where(Task.user_id==user_id))
    db.execute(delete(User).where(User.id == user_id))
    
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User delete is successful!'}