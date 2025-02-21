from pydantic import BaseModel

class Dialogue(BaseModel):
    character: str
    dialogue: str
