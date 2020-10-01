from pydantic import BaseModel
from typing import List


class Runcommands_Hosts(BaseModel):
    host: str
    username: str
    password: str
    device_type: str
    port: int
    command: str


class Runcommands_model(BaseModel):
    hosts: List[Runcommands_Hosts]
