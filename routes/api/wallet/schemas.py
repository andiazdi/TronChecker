from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from decimal import Decimal


class WalletInfoSchema(BaseModel):
    address: str
    balance: Decimal
    bandwidth: int
    energy: int


class WalletInDB(WalletInfoSchema):
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)


class WalletAddressSchema(BaseModel):
    address: str
