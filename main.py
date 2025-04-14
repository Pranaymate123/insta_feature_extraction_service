from fastapi import FastAPI, HTTPException
from app.errors import ERRORS
from app.exception_handler import invalid_url_exception_handler
from app.exceptions import InvalidUrlException
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
        # Validate the URLs first
        for url in request.profile_urls:
            if not url.startswith("https://www.instagram.com/"):
                logging.error(f"Invalid URL: {url}")
                raise InvalidUrlException(
                    code=ERRORS["INVALID_URL"]["code"],
                    message=ERRORS["INVALID_URL"]["message"],
                    details="Expected Instagram profile URL."
                )

        # Fetch features for all profiles in one batch (via Apify Actor)
        logging.info(f"Processing {len(request.profile_urls)} profiles...")

        features_list = await extract_features_from_instagram(request.profile_urls)

        # Send the features list to the prediction service
        prediction_request = BulkProfilesRequest(profiles=features_list)
        prediction_response = await predict_profiles(prediction_request)

        return prediction_response

    except InvalidUrlException as e:
        raise e

    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred while processing profiles.")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)

# Register custom exception handler
app.add_exception_handler(InvalidUrlException, invalid_url_exception_handler)
