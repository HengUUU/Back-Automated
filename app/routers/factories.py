from fastapi import APIRouter, HTTPException, Query, Body
from app.models.factories_info_model import Factory, FactoryUpdate
from app.services.factories_service import (
    load_factories,
    add_factory,
    update_factory_by_name,
    delete_factory_by_name,
    search_factories_by_name
)

router_factories = APIRouter(prefix="/factories", tags=["factories"])


@router_factories.get("/", response_model=list[Factory])
def get_factories():
    return load_factories()


@router_factories.post("/", response_model=Factory)
def create_factory(factory: Factory):
    try:
        return add_factory(factory)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router_factories.put("/", response_model=Factory)
def modify_factory(name: str = Query(..., description="Factory name to update"), factory: Factory = None):
    try:
        return update_factory_by_name(name, factory)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router_factories.delete("/", response_model=dict)
def remove_factory(name: str = Query(..., description="Factory name to delete")):
    try:
        delete_factory_by_name(name)
        return {"message": "Factory deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router_factories.get("/search", response_model=list[Factory])
def search_factories(name: str = Query(..., description="Factory name or partial name to search")):
    results = search_factories_by_name(name)
    if not results:
        raise HTTPException(status_code=404, detail="No factories found with this name")
    return results


@router_factories.patch("/", response_model=Factory)
def update_factory_partial(
    name: str = Query(..., description="Factory name to update"),
    factory: FactoryUpdate = Body(...)
):
    try:
        return update_factory_by_name(name, factory)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
