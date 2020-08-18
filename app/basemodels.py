from pydantic import BaseModel
from typing import List


class Runcommands_Hosts(BaseModel):
    host: str
    username: str
    password: str
    device_type: str
    port: int
    command: str


# CURRENTLY NOT IN USE.
# class Configure_Hosts(BaseModel):
#     host: str
#     username: str
#     password: str
#     device_type: str
#     port: int


# class Scp_Hosts(BaseModel):
#     host: str
#     username: str
#     password: str
#     device_type: str
#     port: int
#     location: str


class Runcommands_model(BaseModel):
    hosts: List[Runcommands_Hosts]


# CURRENTLY NOT IN USE DUE.
# class Configure_model(BaseModel):
#     hosts: List[Configure_Hosts]


# class Scp_model(BaseModel):
#     hosts: List[Scp_Hosts]
