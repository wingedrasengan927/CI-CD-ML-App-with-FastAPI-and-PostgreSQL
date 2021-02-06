from typing import List
from fastapi import Depends, FastAPI, HTTPException

from sqlalchemy.orm import Session
from schemas import Customer, CustomerBase, CustomerUpdate, Review, ReviewCreate
from sentiment_model_inference import get_sentiment

import sys
from os.path import dirname, abspath, join

sys.path.append(abspath(join(dirname(__file__), "database")))

from base import SessionLocal, engine, Base
from queries import create_customer_db, get_customer_db, \
    update_customer_db, get_customer_by_email_db, get_all_customers_db, \
    delete_customer_db, get_customer_reviews_db, get_customer_recent_review_db, \
    add_customer_review_db

app = FastAPI()

@app.on_event("startup")
def connect():
    Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Customer

@app.get("/customers/{customer_id}", response_model=Customer)
def get_customer(customer_id: int, session: Session = Depends(get_db)):
    db_customer = get_customer_db(session, customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@app.get("/customers/email/{customer_email}", response_model=Customer)
def get_customer_by_email(customer_email: str, session: Session = Depends(get_db)):
    db_customer = get_customer_by_email_db(session, customer_email)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@app.get("/customers/", response_model=List[Customer])
def get_all_customers(session: Session = Depends(get_db)):
    return get_all_customers_db(session)

@app.post("/customers/", response_model=Customer)
def create_customer(customer: CustomerBase, session: Session = Depends(get_db)):
    db_customer = get_customer_by_email_db(session, customer.email)
    if db_customer:
        raise HTTPException(status_code=400, detail="Customer already registered")
    return create_customer_db(session, customer.name, customer.email, customer.mobile_number)

@app.put("/customers/{customer_id}", response_model=Customer)
def update_customer(customer_id: int, customer_update: CustomerUpdate, session: Session = Depends(get_db)):
    db_customer = get_customer_db(session, customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return update_customer_db(session, db_customer, customer_update)

@app.delete("/customers/{customer_id}", response_model=Customer)
def delete_customer(customer_id: int, session: Session = Depends(get_db)):
    db_customer = get_customer_db(session, customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return delete_customer_db(session, db_customer)

# Review

@app.get("/customers/{customer_id}/reviews", response_model=List[Review])
def get_customer_reviews(customer_id: int, session: Session = Depends(get_db)):
    reviews = get_customer_reviews_db(session, customer_id)
    if len(reviews) == 0:
        raise HTTPException(status_code=404, detail="No reviews by the customer")
    return reviews

@app.get("/customers/{customer_id}/recent_review", response_model=Review)
def get_customer_recent_review(customer_id: int, session: Session = Depends(get_db)):
    recent_review = get_customer_recent_review_db(session, customer_id)
    if recent_review is None:
        raise HTTPException(status_code=404, detail="No reviews by the customer")
    return recent_review

@app.post("/customers/{customer_id}/reviews", response_model=Review)
def add_customer_review(customer_id: int, review_data: ReviewCreate, session: Session = Depends(get_db)):
    db_customer = get_customer_db(session, customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    review = review_data.review
    rating = get_sentiment(review)
    review = add_customer_review_db(session, db_customer, review, rating)
    return review