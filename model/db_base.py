from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Base Class
Base = declarative_base()

# base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# path of db
DB_PATH = os.path.join(BASE_DIR, 'UniSupport.db')

# create db engine
engine = create_engine(f'sqlite:///{DB_PATH}', echo=True)

# connection pool
Session = sessionmaker(bind=engine)
session = Session()

# test the path of db
print(f"数据库文件路径: {DB_PATH}")