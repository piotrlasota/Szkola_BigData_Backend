from pydantic import BaseModel

class ConcretePredictionResponse(BaseModel):
    request_id: str
    model: str
    prediction: float
    status: str