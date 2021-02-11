import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

USERNAME = os.environ.get("POSTGRES_USER", "mypguser")
PASSWORD = os.environ.get("POSTGRES_PASSWORD", "mypgpassword")
PORT = os.environ.get("PORT", "5432")
DBNAME = os.environ.get("POSTGRES_DB", "customer_reviews")
HOST_NAME = os.environ.get("HOST_NAME", "db")

engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(USERNAME, PASSWORD, HOST_NAME, PORT, DBNAME))
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()