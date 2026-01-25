from pydantic import BaseModel
from typing import Optional

class ContextUpdate(BaseModel):
    content: str = ...  # The new information to add to context

    class Config:
        frozen = True