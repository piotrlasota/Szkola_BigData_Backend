from pydantic import BaseModel

class ConcretePredictionResponse(BaseModel):
    request_id: str
    model: str
    prediction: str
    status: str