from fastapi import APIRouter, HTTPException
from pydantic import BaseModel,Field
import boto3
import os
import uuid
from typing import List

router = APIRouter()

AWS_REGION = os.getenv('AWS_REGION', 'eu-north-1')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
SQS_QUEUE_URL = os.getenv('SQS_QUEUE_URL')

sqs_client = boto3.client(
    'sqs',
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

class UserInteraction(BaseModel):
    date: str
    user_id: str
    session_id: str
    page_type: str
    item_id: str
    category: List[str]
    product_price: float
    old_product_price: float

class InteractionResponse(BaseModel):
    status: str
    message_id: str


@router.post("/user-interaction", response_model=InteractionResponse)
def user_interaction(interaction: UserInteraction):
    deduplication_id = str(uuid.uuid4())
    try:
        # Send message to SQS
        response = sqs_client.send_message(
            QueueUrl=SQS_QUEUE_URL,
            MessageBody=interaction.json(),
            MessageGroupId="user-interactions",
            MessageDeduplicationId=deduplication_id
        )
        return {"status": "Message sent", "message_id": response['MessageId']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
