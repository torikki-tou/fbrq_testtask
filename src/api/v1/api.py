from fastapi import APIRouter

from src.api.v1.endpoints import mailing, client


router = APIRouter()
router.include_router(
    router=mailing.router, prefix='/mailing', tags=['mailing'])
router.include_router(
    router=client.router, prefix='/client', tags=['client'])
