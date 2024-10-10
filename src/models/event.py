from pydantic import BaseModel
from typing import Optional

class Event(BaseModel):
    event_type: str
    timestamp: int
    source_ip: str
    destination_ip: str
    severity: str
    description: str
    user_id: str
    device_id: str
    risk_level: Optional[str] = None
    analysis: Optional[str] = None
    action: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "event_type": "login_attempt",
                "timestamp": 1623456789,
                "source_ip": "192.168.1.100",
                "destination_ip": "10.0.0.1",
                "severity": "medium",
                "description": "Failed login attempt from unusual location",
                "user_id": "user_1234",
                "device_id": "device_567",
                "risk_level": "medium",
                "analysis": "Potential unauthorized access attempt",
                "action": "Block source IP and notify admin"
            }
        }
