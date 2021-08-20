from fastapi import APIRouter, Depends
from requests import Response

from app.operations.models import ExtractBase
from app.operations.services import ExtractService

router = APIRouter(tags=['Operations'], prefix='/extract')


@router.get('/all/')
def list_extracts(service: ExtractService = Depends()):
    return service.get_all()


@router.post('/create/')
def create_extracts(extract: ExtractBase, service: ExtractService = Depends()):
    return service.create(extract)


@router.get("/get/{id}", response_model=ExtractBase)
def get_one(id, service: ExtractService = Depends()):
    return service.get(id)


@router.delete("/delete/{id}")
def delete(id, service: ExtractService = Depends()):
    service.delete(id)
    return Response(status_code=204)


@router.patch('/update/{id}', response_model=ExtractBase)
def update(id, data: ExtractBase, service: ExtractService = Depends()):
    return service.update(id, data)
