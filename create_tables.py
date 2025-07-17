# create_tables.py
from database import engine
from models.model import Base

Base.metadata.create_all(bind=engine)

print("✅ All tables created in TiDB!")
