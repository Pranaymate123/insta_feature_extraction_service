from fastapi import FastAPI, HTTPException
from app.schemas import ProfileListRequest, BulkProfilesRequest, PredictionResponse
from app.extractor import extract_features_from_instagram
from app.prediction_client import predict_profiles
import logging
import uvicorn

app = FastAPI(title="Instagram Feature Extraction Service")
logging.basicConfig(level=logging.INFO)

@app.post("/extract", response_model=PredictionResponse)
async def extract_profiles(request: ProfileListRequest):
    try:
        features_list = []
        for url in request.profile_urls:
            logging.info(f"Processing profile: {url}")
            features = await extract_features_from_instagram(url)

            if "error" in features:
                logging.error(f"Error extracting features for {url}: {features['error']}")
                raise HTTPException(status_code=400, detail=f"Error processing {url}: {features['error']}")

            features_list.append(features)

        prediction_request = BulkProfilesRequest(profiles=features_list)
        prediction_response = await predict_profiles(prediction_request)
        return prediction_response

    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred while processing profiles.")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
