from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from agent import stream_agent
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class TripRequest(BaseModel):
    destination: str
    days: int
    vibe: str

@app.post("/plan-trip")
async def plan_trip(request: TripRequest):

    def generate():
        for token in stream_agent(request.destination, request.days, request.vibe):
            # SSE format: each chunk must be "data: ...\n\n"
            data = json.dumps({"token": token})
            yield f"data: {data}\n\n"
        # Send a done signal so the frontend knows streaming is finished
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        }
    )
