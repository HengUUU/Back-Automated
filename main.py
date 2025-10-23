from fastapi import FastAPI
import uvicorn
from pydantic  import BaseModel
import os
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv


load_dotenv()

api = FastAPI(title="Automated Poster")

front_url = os.getenv("FRONTEND_URL")


api.add_middleware(
    CORSMiddleware,
    allow_origins=[front_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



from app.routers.data_entry import router
from app.routers.factories import router_factories
api.include_router(router)
api.include_router(router_factories)







