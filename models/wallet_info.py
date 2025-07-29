from dependencies.database import base
from sqlalchemy import Column, Integer, String, UUID, Float, func, DateTime
import uuid


class WalletInfo(base):
    __tablename__ = "wallet_info"

    uuid = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
    )
    address = Column(String, nullable=False)
    balance = Column(Float, nullable=False)
    bandwidth = Column(Integer, nullable=False)
    energy = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=func.current_timestamp())
