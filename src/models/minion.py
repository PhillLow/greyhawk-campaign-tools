from pydantic import BaseModel

class Minion(BaseModel):
    name: str
    creature_type: str # e.g. "Wolf", "Skeleton", "Familiar"
    current_hp: int
    max_hp: int
    notes: str = ""
