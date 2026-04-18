from pydantic import BaseModel, Field
from typing import Optional


class ServiceBase(BaseModel):
    name: str = Field(..., description="Название услуги", example="Массаж спины")
    description: Optional[str] = Field(None, description="Описание услуги")
    price: float = Field(..., description="Цена", example=2500.00)
    duration_minutes: int = Field(..., description="Длительность в минутах", example=60)


class ServiceCreate(ServiceBase):
    pass


class ServiceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    duration_minutes: Optional[int] = None


class ServiceResponse(ServiceBase):
    id: int = Field(..., description="ID услуги")

    class Config:
        orm_mode = True