import sys
from os.path import dirname, abspath, join

sys.path.append(abspath(join(dirname(__file__), "models")))

from customer import Customer
from reviews import Review

def get_customer_db(session, customer_id):
    customer = session.query(Customer).get(customer_id)
    return customer

def get_customer_by_email_db(session, customer_email):
    return session.query(Customer).filter(Customer.email == customer_email).first()

def get_all_customers_db(session):
    return session.query(Customer).all()
  
def get_customer_reviews_db(session, customer_id):
    # TODO: Try with get as we are using customer id
    return session.query(Review).join(Customer).\
            filter(Customer.id == customer_id).all()

def get_customer_recent_review_db(session, customer_id):
    return session.query(Review).join(Customer).\
            filter(Customer.id == customer_id).\
            order_by(Review.review_date.desc()).first()

def create_customer_db(session, name, customer_email, mobile_number):
    customer = Customer(name, customer_email, mobile_number)
    session.add(customer)
    session.commit()
    return customer

def add_customer_review_db(session, customer, review, rating):
    review = Review(review, rating)
    customer.reviews.append(review)
    session.add(review)
    session.commit()
    return review

def update_customer_db(session, customer, update_dictionary):
    for key, val in update_dictionary:
        if val is not None:
            setattr(customer, key, val)
    session.commit()
    return customer
    
def delete_customer_db(session, customer):
    session.delete(customer)
    session.commit()
    return customer