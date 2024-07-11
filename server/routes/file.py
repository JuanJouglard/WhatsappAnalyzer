from typing import Annotated
from fastapi import APIRouter, UploadFile, File, Depends, Query, Security
from services.file import validate, is_valid_uuid, process_file
import uuid


router = APIRouter(prefix="/file", tags=["file"])


def validate_file(file: UploadFile):
    return validate(file)

file_validation = Annotated[UploadFile, Depends(validate_file)]


def get_current_user(user):
    return user

@router.post("/parse")
async def parse(file: bytes = File(...)):
    dataframe = await process_file(file.decode("utf-8"))
    return {"Status": "parsed"}

#TODO: use pydantic for id validation
@router.get("/metrics")
async def get_metrics(file_id: Annotated[str, Depends(is_valid_uuid)]):
    try:
        dataframe = await read_file(file_id)
        return {"Status": "OK", "valid_id": file_id}
    except ValueError:
        raise HTTPException(status_code=500, detail="ID not valid")

