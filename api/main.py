from fastapi import FastAPI
from api.routers import router,profilerouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app=FastAPI()

app.include_router(profilerouter.router)
app.include_router(router.router)


app.add_middleware(

CORSMiddleware,
allow_origins=["*"],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],

)
app.mount("/static", StaticFiles(directory="static"), name="static")

