from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates

from pydantic import validate_email

from base import Base

class Customer(Base):
    __tablename__ = 'customer'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False) 
    email = Column(String(50), nullable=False, unique=True)
    mobile_number = Column(String(20), nullable=False, unique=True)
    # it doesn't matter what name you are giving as backref argument
    reviews = relationship('Review', backref='customer', cascade="all, delete, delete-orphan")

    @validates('mobile_number')
    def no_chars_in_mobile_no(self, key, v):
        if any(i.isalpha() for i in v):
            raise ValueError("Invalid Mobile Number")
        return v

    @validates('email')
    def check_email(self, key, v):
        if not validate_email(v):
            raise ValueError("Invalid Email")
        return v

    def __init__(self, name, email, mobile_number):
        self.name = name
        self.email = email
        self.mobile_number = mobile_number

    def __repr__(self):
        return "Customer({}, {}, {})".format(self.name, self.email, self.mobile_number)
