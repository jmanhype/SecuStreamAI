from sqlalchemy import Column, Integer, String, DateTime, Boolean
from src.db.database import Base
from datetime import datetime

class Event(Base):
    """
    Represents a security event in the system.

    Attributes:
        id (int): Unique identifier for the event.
        event_type (str): Type of the security event (e.g., login_attempt, firewall_alert).
        timestamp (datetime): Time when the event occurred.
        source_ip (str): IP address of the event source.
        destination_ip (str): IP address of the event destination.
        severity (str): Severity level of the event.
        description (str): Detailed description of the event.
        user_id (str): Identifier of the user associated with the event.
        device_id (str): Identifier of the device associated with the event.
        risk_level (str, optional): Assessed risk level of the event.
        analysis (str, optional): Analysis results of the event.
        action (str, optional): Action taken in response to the event.
    """
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String, index=True, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    source_ip = Column(String, nullable=False)
    destination_ip = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    description = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    device_id = Column(String, nullable=False)
    risk_level = Column(String, nullable=True)
    analysis = Column(String, nullable=True)
    action = Column(String, nullable=True)

class User(Base):
    """
    Represents a user account in the system.

    Attributes:
        id (int): Unique identifier for the user.
        username (str): Unique username for the user.
        hashed_password (str): Hashed password for user authentication.
        disabled (bool): Flag indicating if the user account is disabled.
        created_at (datetime): Timestamp of when the user account was created.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    disabled = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)