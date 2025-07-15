from pydantic import BaseModel

class ComplaintCreate(BaseModel):
    text: str

class ComplaintResponse(BaseModel):
    id: int
    status: str
    sentiment: str
    category: str
    country: str
    is_spam: bool

    class Config:
        orm_mode = True


