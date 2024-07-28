import json
import boto3
import os
from datetime import datetime
from sqlalchemy import create_engine, Column, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uuid
import numpy as np

S3_BUCKET = os.getenv('S3_BUCKET')
DATABASE_URL = os.getenv('DATABASE_URL')

s3_client = boto3.client('s3')

# Define the SQLAlchemy Base and UserInteractionDB model
Base = declarative_base()

class UserInteractionDB(Base):
    __tablename__ = 'user_interactions'
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    date = Column(DateTime)
    user_id = Column(String, index=True)
    session_id = Column(String, index=True)
    page_type = Column(String, nullable=True)
    item_id = Column(String, nullable=True)
    category = Column(String, nullable=True)  
    product_price = Column(Float, nullable=True)
    old_product_price = Column(Float, nullable=True)

# Create the database engine
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def lambda_handler(event, context):
    session = Session()
    try:
        for record in event['Records']:
            message = json.loads(record['body'])
           
            interaction_date_str = message.get('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            interaction_date = datetime.strptime(interaction_date_str, '%Y-%m-%d %H:%M:%S')
        
            user_id = message.get('user_id', None)
            session_id = message.get('session_id', None)
            file_name = f'interactions/{user_id}/{session_id}/{interaction_date.strftime("%Y-%m-%d_%H-%M-%S")}.json'
            
            s3_client.put_object(
                Bucket=S3_BUCKET,
                Key=file_name,
                Body=json.dumps(message),
                ContentType='application/json'
            )
            
            unique_id = str(uuid.uuid4())
            
            # Save to AWS RDS
            user_interaction = UserInteractionDB(
                id=unique_id,
                date=interaction_date,
                user_id=user_id,
                session_id=session_id,
                page_type=message.get('page_type', None),
                item_id=message.get('item_id', None),
                category=json.dumps(message.get('category', [])),
                product_price=message.get('product_price', np.nan),
                old_product_price=message.get('old_product_price', np.nan)
            )
            session.add(user_interaction)
            session.commit()
        
        return {
            'statusCode': 200,
            'body': json.dumps('Successfully processed and saved user interactions.')
        }
    except Exception as e:
        print(e)
        session.rollback()
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error processing user interactions: {str(e)}')
        }
    finally:
        session.close()

