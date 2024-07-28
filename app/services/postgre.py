import os
from sqlalchemy import create_engine, Column, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uuid
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
import logging
from datetime import datetime, timezone
from sqlalchemy import desc

DATABASE_URL = os.getenv('DATABASE_URL')  

# class ModelStatus(Enum):
#     STARTED = 'Started'
#     COMPLETED = 'Completed'
#     ONGOING = 'Ongoing'
#     ERROR = 'Error'

Base = declarative_base()


class ModelTrain(Base):
    __tablename__ = 'model_train'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    status = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    train_auc = Column(Float, nullable=True)
    test_auc = Column(Float, nullable=True)
    train_precision = Column(Float, nullable=True)
    test_precision = Column(Float, nullable=True)
    train_recall = Column(Float, nullable=True)
    test_recall = Column(Float, nullable=True)

engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)

def insert_model_train():
   
    session = Session()  
    try:
        new_model = ModelTrain(status="started", description=None)
        session.add(new_model)
        session.commit()
        return new_model.id
    except SQLAlchemyError as e:
        session.rollback() 
        raise e  
        session.close()

from sqlalchemy.exc import SQLAlchemyError

def get_model_train(model_id):
   
    session = Session()
    try:
        train_record = session.query(ModelTrain).filter_by(id=model_id).first()
        return train_record
    except SQLAlchemyError as e:
        raise e
    finally:
        session.close()

def get_latest_train_model():
    session = Session()
    try:
        train_record = session.query(ModelTrain).filter(
            ModelTrain.status == "completed"
        ).order_by(desc(ModelTrain.created_at)).first()
        
        return train_record
    except SQLAlchemyError as e:
        print(f"Database error occurred: {e}")
        raise
    finally:
        session.close()

def get_completed_train_models(page: int = 1, page_size: int = 10):
    session = Session()

    try:
        offset = (page - 1) * page_size

        train_records = session.query(ModelTrain).filter(
            ModelTrain.status == "completed"
        ).order_by(desc(ModelTrain.created_at)).offset(offset).limit(page_size).all()
        
        return train_records
    except SQLAlchemyError as e:
        print(f"Database error occurred: {e}")
        raise
    finally:
        session.close()

def update_model_train(version_id: str, status: str, description: str, metrics=None):
    session = Session()
    try:
        train_record = session.query(ModelTrain).filter_by(id=version_id).first()
        if train_record:
            train_record.status = status
            train_record.description = description

            if metrics:
                train_record.train_auc = metrics.get('train_auc', None)
                train_record.test_auc = metrics.get('test_auc', None)
                train_record.train_precision = metrics.get('train_precision', None)
                train_record.test_precision = metrics.get('test_precision', None)
                train_record.train_recall = metrics.get('train_recall', None)
                train_record.test_recall = metrics.get('test_recall', None)
    
            session.commit()
            return {"message": f"Record {version_id} updated successfully."}
        else:
            return {"message": "Record not found."}
    except SQLAlchemyError as e:
        session.rollback()
        logging.error(f"Failed to update record: {e}")  # Log the exception
        raise
    finally:
        session.close()
