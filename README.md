# CI-CD-ML-App-with-FastAPI-and-PostgreSQL

An application to store customer data and customer reviews in a PostgreSQL database and perform CRUD operations on them using FastAPI and SQLAlchemy. A sentiment analysis model is used to predict the sentiment of a customer review. It includes Pydantic data validation and SQLAlchemy data validation

## Getting Started

### running locally
Create a virtual environment and run  
`pip install -r requirements.txt`

### Run tests locally
install pytest `pip install pytest`  
run `pytest tests`

### Run the application using Docker
run `docker-compose up`  
This will start a PostgreSQL instance and the application instance  
you can connect to the database from the command line using psql  
to view the swagger documentation of the application, go to `localhost:8002/docs`  
you can test the application there
