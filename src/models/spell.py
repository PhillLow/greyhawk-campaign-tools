from pydantic import BaseModel
from enum import Enum
from typing import List

class School(str, Enum):
    ABJURATION = "Abjuration"
    CONJURATION = "Conjuration"
    DIVINATION = "Divination"
    ENCHANTMENT = "Enchantment"
    EVOCATION = "Evocation"
    ILLUSION = "Illusion"
    NECROMANCY = "Necromancy"
    TRANSMUTATION = "Transmutation"

class Spell(BaseModel):
    name: str
    level: int # 0 = Cantrip
    school: School
    casting_time: str = "1 Action"
    range: str = "60 feet"
    components: str = "V, S"
    duration: str = "Instantaneous"
    concentration: bool = False
    ritual: bool = False
    description: str
    prepared: bool = False
    classes: List[str] = []
