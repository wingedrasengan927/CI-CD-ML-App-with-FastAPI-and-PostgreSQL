from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

from main import app, get_db
from base import Base

database_url = 'sqlite:///test.db'
engine = create_engine(database_url, connect_args={"check_same_thread": False})
TestSession = sessionmaker(bind=engine)

def override_get_db():
    try:
        db = TestSession()
        yield db
    finally:
        db.close()

@pytest.fixture(scope='session', autouse=True)
def setup_database():
    Base.metadata.create_all(engine)
    app.dependency_overrides[get_db] = override_get_db
    print("Database setup complete.")
    yield
    print("Deleting Database...")
    for table in Base.metadata.sorted_tables:
        engine.execute(table.delete())

@pytest.fixture()
def client():
    return TestClient(app)

def test_create_customers(client):

    customer1 = {"name": "Joe Wink", "email": "joe.wink@email.com", "mobile_number": '+91-9802357891'}
    response = client.post("/customers/", json=customer1)
    assert response.status_code == 200
    data = response.json()

    # performing basic checks
    assert data.get('name') == customer1['name']
    assert data.get('reviews') == [] # reviews should be empty as we haven't added anything
    assert data.get('id') == 1

    # add one more customer
    # notice here
    customer2 = {'name': 'Ellie Huston', 'email': 'ellie.huston@company.com', 'mobile_number': 7081567902}
    client.post("/customers/", json=customer2)

def test_add_invalid_customers(client):

    # Test Field Missing
    invalid_customer1 = {'name': 'amanda carvalho', 'email': 'amanda.carvalho@company.com'}
    response = client.post("/customers/", json=invalid_customer1)
    assert response.status_code == 422

    # Test Invalid Field
    invalid_customer2 = {'name': 'amanda carvalho', 'email': 'invalid email', 'mobile_number': '9407321618'}
    response = client.post("/customers/", json=invalid_customer2)
    assert response.status_code == 422

def test_get_customers(client):
    # get all customers
    response = client.get("/customers/")
    assert response.status_code == 200
    assert len(response.json()) == 2

    # get customer by id
    response = client.get("/customers/1")
    assert response.status_code == 200
    assert response.json().get('name') == 'Joe Wink'

    # get customer by email
    response = client.get("/customers/email/ellie.huston@company.com")
    assert response.status_code == 200
    assert response.json().get('name') == 'Ellie Huston'

    # get invalid customer
    response = client.get("/customers/221")
    assert response.status_code == 404
    assert response.json().get('detail') == 'Customer not found'

def test_update_customers(client):
    # update Joe Wink's mobile number
    update_dictionary = {"mobile_number": '+40-8064329573'}
    client.put("/customers/1", json=update_dictionary)

    # get Joe Wink and check if mobile number has been updated
    response = client.get("/customers/1")
    assert response.json().get('mobile_number') == update_dictionary["mobile_number"]

def test_reviews(client):
    # add reviews for customer 1
    customer1_review1 = {"review": "Had a great experience!"}
    customer1_review2 = {"review": "Never fails to reach my expectations."}

    client.post("/customers/1/reviews", json=customer1_review1)
    client.post("/customers/1/reviews", json=customer1_review2)

    # get all customer 1 reviews
    response = client.get("/customers/1/reviews")
    assert response.status_code == 200
    assert len(response.json()) == 2

    # get latest review
    response = client.get("/customers/1/recent_review")
    assert response.status_code == 200
    data = response.json()
    assert data.get('review') == customer1_review2['review']
    # check if the review is by customer 1
    assert data.get('customer_id') == 1

    # add review for customer 2
    customer2_review1 = {"review": "Wonderful Place!"}
    client.post("/customers/2/reviews", json=customer2_review1)

def test_delete_customer(client):
    # delete joe wink
    client.delete("/customers/1")

    # check total customers
    response = client.get("/customers")
    assert len(response.json()) == 1

    # check if joe wink's reviews have been deleted
    response = client.get("/customers/1/reviews")
    assert response.status_code == 404

    # check if ellie's id (primary key) hasn't changed now that joe has been deleted
    # check if joe wink's reviews have been deleted
    response = client.get("/customers/2")
    assert response.json().get('name') == 'Ellie Huston'