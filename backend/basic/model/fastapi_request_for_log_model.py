from pydantic import BaseModel, Field
from typing import Dict, Optional, List, Tuple
from fastapi import Request


class FastApiRequestForLogModel(BaseModel):
    headers: Optional[List] = Field(None, title="Headers")
    query_params: Optional[Dict] = Field(None, title="Query Params")
    path_params: Optional[Dict] = Field(None, title="Path Params")
    client: Optional[Tuple[str, int]] = Field(None, title="Client")
    method: Optional[str] = Field(None, title="Method")
    url: Optional[str] = Field(None, title="Url")
    cookies: Optional[Dict] = Field(None, title="Cookies")

    @classmethod
    def init(cls, request: Request) -> "FastApiRequestForLogModel":
        return cls(
            headers=request.headers.items(),
            query_params=dict(request.query_params),
            path_params=dict(request.path_params),
            client=(request.client.host, request.client.port),
            method=request.method,
            url=str(request.url),
            cookies=dict(request.cookies),
        )
