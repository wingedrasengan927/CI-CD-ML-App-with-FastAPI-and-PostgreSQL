import datetime
from typing import List, Optional

from pydantic import BaseModel, validator, validate_email

class Review(BaseModel):
    id: int
    review: str
    rating: float
    review_date: datetime.date
    customer_id: int

    class Config:
        orm_mode = True

class ReviewCreate(BaseModel):
    review: str

class CustomerBase(BaseModel):
    name: str
    email: str
    mobile_number: str

    @validator('mobile_number')
    def no_chars_in_mobile_no(cls, v):
        if any(i.isalpha() for i in v):
            raise ValueError("Invalid Mobile Number")
        return v

    @validator('email')
    def check_email(cls, v):
        if not validate_email(v):
            raise ValueError("Invalid Email")
        return v

class Customer(CustomerBase):
    id: int
    reviews: List[Review] = []

    class Config:
        orm_mode = True 

class CustomerUpdate(CustomerBase):
    email: Optional[str] = None
    name: Optional[str] = None
    mobile_number: Optional[str] = None