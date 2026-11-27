"""
/main.py 

Defines the starting point of the FastAPI application. Provides information
about the different routers, exceptions and middlewares involved. 
"""

# Importing the necessary modules 
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

# Importing from local modules 
from core.exceptions import APIException
from core.response_model import ResponseModel, APIResponse

app = FastAPI(
    title = "Aperio API",
    summary = "Backend of an efficient research platform",
    version = "0.0.1",
    )

@app.exception_handler(APIException)
def handle_exception(request: Request, exception_data: APIException) -> JSONResponse:
    return ResponseModel(
        server_status_code = exception_data.server_status_code,
        request_id = getattr(request.state, "request_id", "unknown"),
        api_url = str(request.url),
        api_data = APIResponse(
            api_status_code = exception_data.api_status_code,
            api_status_message = exception_data.api_status_message,
            data = exception_data.data
        )
    ).to_json_response()
