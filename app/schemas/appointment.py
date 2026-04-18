from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class AppointmentBase(BaseModel):
    service_id: int = Field(..., description="ID услуги")
    appointment_time: datetime = Field(..., description="Время записи")


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentUpdate(BaseModel):
    appointment_time: Optional[datetime] = None
    status: Optional[str] = None


class AppointmentResponse(AppointmentBase):
    id: int = Field(..., description="ID записи")
    user_id: int = Field(..., description="ID пользователя")
    created_at: datetime = Field(..., description="Дата создания")
    status: str = Field("pending", description="Статус записи")

    class Config:
        orm_mode = True