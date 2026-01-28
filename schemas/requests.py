from pydantic import BaseModel

class ConcreteIngredientsPayload(BaseModel):
    Cement: float
    BlastFurnaceSlag: float
    FlyAsh: float
    Water: float
    Superplasticizer: float
    CoarseAggregate: float
    FineAggregate: float
    Age: float

class ConcretePredictionRequest(BaseModel):
    request_id: str
    model: str
    payload: ConcreteIngredientsPayload