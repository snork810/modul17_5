from fastapi import FastAPI
from routers import task_routers, user_routers
app = FastAPI()

@app.get('/')
async def welcome():
    return {'message':'Welcome to Taskmanager'}

app.include_router(task_routers.router)
app.include_router(user_routers.router)