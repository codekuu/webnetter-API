from pydantic import BaseModel
from typing import List


class host_data_runcommands(BaseModel):
    host: str
    username: str
    password: str
    device_type: str
    port: int
    command: str


class runcommands_request_model(BaseModel):
    hosts: List[host_data_runcommands]


class general_response_dict(BaseModel):
    success: bool
    host: str
    software: str
    output: str


class general_response_model(BaseModel):
    status: str
    data: List[general_response_dict]
    outputFromAll: str
