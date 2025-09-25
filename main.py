from fastapi import FastAPI
import uvicorn
from pydantic  import BaseModel

from fastapi.middleware.cors import CORSMiddleware

api = FastAPI(title="Automated Poster")



api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # allow_origins=[
    #     "http://localhost:3000",
    #     "http://frontend:3000",
    #     "https://65j8kfdv-3000.asse.devtunnels.ms",
    #     "http://127.0.0.1:3000"
    #                ],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


from app.routers.data_entry import router
from app.routers.factories import router_factories
api.include_router(router)
api.include_router(router_factories)


@api.get('/')
def index():
    return {'message':'Hello my fbro'}





