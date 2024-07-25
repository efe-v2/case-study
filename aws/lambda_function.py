import json
import boto3
import os
from datetime import datetime

s3_client = boto3.client('s3')
S3_BUCKET = os.getenv('S3_BUCKET')

def lambda_handler(event, context):
    try:
        for record in event['Records']:
            
            message = json.loads(record['body'])
            
            user_id = message['user_id']
            session_id = message['session_id']
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            file_name = f'interactions/{user_id}/{session_id}/{timestamp}.json'
            
            s3_client.put_object(
                Bucket=S3_BUCKET,
                Key=file_name,
                Body=json.dumps(message),
                ContentType='application/json'
            )
        
        return {
            'statusCode': 200,
            'body': json.dumps('Successfully processed and saved user interactions.')
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error processing user interactions: {str(e)}')
        }
