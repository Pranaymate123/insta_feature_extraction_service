from fastapi import FastAPI, HTTPException
from app.schemas import ProfileListRequest, FeatureResponse
from app.extractor import extract_features_from_instagram
from typing import List
import logging
import uvicorn  # ✅ Add this

# Initialize FastAPI app
app = FastAPI(title="Instagram Feature Extraction Service")

# Set up logging
logging.basicConfig(level=logging.INFO)

@app.post("/extract", response_model=List[FeatureResponse])
async def extract_profiles(request: ProfileListRequest):
    try:
        # Extract features for each Instagram profile URL
        results = []
        for url in request.profile_urls:
            logging.info(f"Processing profile: {url}")
            features = await extract_features_from_instagram(url)

            if "error" in features:
                # If there's an error, return a 400 response with the error message
                logging.error(f"Error extracting features for {url}: {features['error']}")
                raise HTTPException(status_code=400, detail=f"Error processing {url}: {features['error']}")

            # Append the features if no error occurred
            results.append(features)

        return results

    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred while processing profiles.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)

    # Command use to run this python main.py ( Will take port 8001)
    # uvicorn main:app --port 8001 --reload (manual option )