from sqlalchemy import Column, String, Float, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uuid

Base = declarative_base()

class UserInteractionDB(Base):
    __tablename__ = 'user_interactions'
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    date = Column(DateTime)
    user_id = Column(String, index=True, nullable=True)
    session_id = Column(String, index=True, nullable=True)
    page_type = Column(String, nullable=True)
    item_id = Column(String, nullable=True)
    category = Column(String, nullable=True)  
    product_price = Column(Float, nullable=True)
    old_product_price = Column(Float, nullable=True)

def create_table(database_url):

    engine = create_engine(database_url)

    # Create the table in the database
    Base.metadata.create_all(engine)

    print("Table created successfully.")
