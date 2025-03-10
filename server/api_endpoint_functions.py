from fastapi import  APIRouter
import asyncio

router = APIRouter()

@router.post("/")
async def upload_file():
    pass
