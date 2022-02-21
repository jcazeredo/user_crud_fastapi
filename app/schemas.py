from enum import Enum
from pydantic import BaseModel


class TVShow(str, Enum):
    breaking_bad = "breaking_bad"
    the_wire = "the_wire"


class User(BaseModel):
    id: int
    name: str
    favorite_tv_show: TVShow

    class Config:
        orm_mode = True
