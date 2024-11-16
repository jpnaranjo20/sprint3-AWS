import os
from typing import List

from app import db
from app import settings as config
from app import utils
from app.auth.jwt import get_current_user
from app.model.schema import PredictRequest, PredictResponse
from app.model.services import model_predict
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

router = APIRouter(tags=["Model"], prefix="/model")

@router.post("/predict")
async def predict(file: UploadFile, current_user=Depends(get_current_user)):
    rpse = {"success": False, "prediction": None, "score": None}
    # To correctly implement this endpoint you should:
    #   1. Check a file was sent and that file is an image, see `allowed_file()` from `utils.py`.
    #   2. Store the image to disk, calculate hash (see `get_file_hash()` from `utils.py`) before
    #      to avoid re-writing an image already uploaded.
    #   3. Send the file to be processed by the `model` service, see `model_predict()` from `services.py`.
    #   4. Update and return `rpse` dict with the corresponding values
    # If user sends an invalid request (e.g. no file provided) this endpoint
    # should return `rpse` dict with default values HTTP 400 Bad Request code

    # rpse["success"] = None
    # rpse["prediction"] = None
    # rpse["score"] = None
    # rpse["image_file_name"] = None
    if not file or not utils.allowed_file(file.filename):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File type is not supported."
        )

    hashed_name = await utils.get_file_hash(file)
    file_path = os.path.join(config.UPLOAD_FOLDER, hashed_name)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    prediction, score = await model_predict(hashed_name)
    rpse.update({
        "success": True,
        "prediction": prediction,
        "score": score,
        "image_file_name": str(hashed_name)
    })

    return PredictResponse(**rpse)
