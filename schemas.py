from pydantic import BaseModel
from typing import List, Optional,Dict
from datetime import date

class Action(BaseModel):
    Game: str
    Team: str
    Name: str
    Nr: str
    Text: str
    PLTime: str