from fastapi import HTTPException

class EventNotFoundException(HTTPException):
    def __init__(self, event_id: int):
        super().__init__(status_code=404, detail=f"Event with id {event_id} not found")

class InvalidEventDataException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=detail)