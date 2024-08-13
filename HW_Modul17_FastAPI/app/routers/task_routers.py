from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from backend.db_depends import get_db
from typing import Annotated
from models.task_model import Task
from models.user_model import User
from schemas import CreateTask, UpdateTask
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter(prefix='/task', tags=['task'])

@router.get('/')
async def all_tasks(db:Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task).all()
    return tasks

@router.get('/task_id')
async def task_by_id(db:Annotated[Session, Depends(get_db)], task_id):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Task was not found')
    return task

@router.post('/create')
async def create_task(db:Annotated[Session, Depends(get_db)], create_task_model:CreateTask, user_id):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User was not found')
    db.execute(insert(Task).values(title=create_task_model.title,
                                   content=create_task_model.content,
                                   priority=create_task_model.priority,
                                   user_id=user_id,
                                   slug=slugify(create_task_model.title)))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}
    

@router.put('/update')
async def update_task(db:Annotated[Session, Depends(get_db)], user_id, update_task_model:UpdateTask):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User was not found')
    db.execute(update(Task).where(Task.user_id==user_id).values(title=update_task_model.title,
                                   content=update_task_model.content,
                                   priority=update_task_model.priority,
                                   completed=update_task_model.completed,
                                   slug=slugify(update_task_model.title)))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'Successful'}
    

@router.delete('/delete')
async def delete_task(db:Annotated[Session, Depends(get_db)], user_id):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User was not found')
    db.execute(delete(Task).where(Task.user_id==user_id))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'Successful'}
