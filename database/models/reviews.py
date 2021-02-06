from sqlalchemy import Column, Integer, DateTime, Text, Float, ForeignKey
from datetime import datetime

from base import Base

class Review(Base):

    __tablename__ = "reviews"

    id = Column(Integer, primary_key = True)
    review = Column(Text)
    rating = Column(Float)
    review_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    # basically, the Foreign Key parameter specifies on what column to join
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)

    def __init__(self, review=None, rating=None):
        self.review = review
        self.rating = rating

    def __repr__(self):
        return 'Review({}, {})'.format(self.review, self.rating)