from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

user = os.getenv("DB_USER")
password = os.getenv("DB_PASS")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
db = os.getenv("DB_NAME")
ca_path = os.getenv("DB_CA")

if not os.path.isfile(ca_path):
    raise FileNotFoundError(f"SSL CA file not found at {ca_path}")

SQLALCHEMY_DATABASE_URL = (
    f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}?ssl_ca={ca_path}"
)

connect_args = {"ssl": {"ca": ca_path}}

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
