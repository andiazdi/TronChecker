from fastapi import Depends
from pydantic import BaseModel, Field
from typing import Annotated


class PaginationParams(BaseModel):
    page: int = Field(1, ge=1)
    per_page: int = Field(10, ge=1, le=100)


PaginationParamsDep = Annotated[PaginationParams, Depends(PaginationParams)]
