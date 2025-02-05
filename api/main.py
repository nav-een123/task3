from fastapi import FastAPI
from api.routers import route,task

app=FastAPI()

app.include_router(route.router)
app.include_router(task.router)
