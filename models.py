from pydantic import BaseModel
from pydantic.config import ConfigDict


class BirdCreate(BaseModel):
  name: str


class BirdUpdate(BaseModel):
  id: int
  name: str


class BirdResponse(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  name: str
