from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from kafka import KafkaProducer
from contextlib import asynccontextmanager

from kafka_utils import config as kafka_config
from schemas.requests import ConcretePredictionRequest
from schemas.responses import ConcretePredictionResponse
from services import kafka_consumer_service, kafka_producer_service

kafka_producer: KafkaProducer | None = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global kafka_producer
    # startup
    kafka_producer = kafka_config.create_producer()
    yield
    # shutdown
    if kafka_producer is not None:
        kafka_producer.flush()
        kafka_producer.close()
        kafka_producer = None


app = FastAPI(title="Concrete Strength Inference API", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    
@app.post("/ConcretePrediction", response_model=ConcretePredictionResponse)
def infer(req: ConcretePredictionRequest):
    if req.model != "concrete_strength_v1":
        raise HTTPException(
            status_code=400,
            detail="Unsupported model"
        )
    kafka_request = {
        "request_id": req.request_id,
        "model": req.model,
        "payload": req.payload.model_dump()
    }
    global kafka_producer
    if kafka_producer is None:
        raise HTTPException(status_code=500, detail="Kafka producer not initialized")
    try:
        if kafka_producer is not None:
            kafka_producer_service.send(kafka_producer, req.request_id, kafka_request)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Kafka send failed: {e}")
    
    try:
        data = kafka_consumer_service.wait_for_response(req.request_id, req.model)
    except TimeoutError as e:
        raise HTTPException(status_code=504, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Kafka receive failed: {e}")
    
    return ConcretePredictionResponse(
        request_id=data["request_id"],
        model=data["model"],
        prediction=str(data["prediction"]),
        status=data.get("status", "OK")
    )
