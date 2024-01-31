import re
from fastapi.responses import JSONResponse

def extract_session_id(session_str:str):
    pattern = r"sessions/(\w+?)/"

    match = re.search(pattern, session_str)

    if match:
        desired_substring = match.group(1)
        return desired_substring
    else:
        return "Match not found."

def json_response(fulfillment: str):
    return JSONResponse(content={
        "fulfillmentText": fulfillment
    })