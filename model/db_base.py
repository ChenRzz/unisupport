from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Base class for declarative models
Base = declarative_base()

# Base directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Path to the SQLite database file
DB_PATH = os.path.join(BASE_DIR, 'UniSupport.db')

# Create the database engine
engine = create_engine(f'sqlite:///{DB_PATH}', echo=True)

# Create a session factory and initialize a session
Session = sessionmaker(bind=engine)
session = Session()

# Print the path of the database file for debugging
print(f"Database file path: {DB_PATH}")
