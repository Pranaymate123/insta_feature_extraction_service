import httpx
import logging
from app.config import PREDICTION_SERVICE_URL
from app.schemas import BulkProfilesRequest, PredictionResponse

logging.basicConfig(level=logging.INFO)

async def predict_profiles(request_data: BulkProfilesRequest) -> PredictionResponse:
    url = f"{PREDICTION_SERVICE_URL}/predict-profiles"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=request_data.dict())
            response.raise_for_status()
            return PredictionResponse(**response.json())
    except Exception as e:
        logging.error(f"Prediction service error: {e}")
        raise