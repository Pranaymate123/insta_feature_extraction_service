from fastapi import Request
from fastapi.responses import JSONResponse
from app.exceptions import InvalidUrlException

async def invalid_url_exception_handler(request: Request, exc: InvalidUrlException):
    return JSONResponse(
        status_code=400,
        content={
            "code": exc.code,
            "message": exc.message,
            "details": exc.details
        }
    )
