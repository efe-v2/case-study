import boto3
import pickle
import os

S3_BUCKET = os.getenv('S3_BUCKET')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION', 'eu-north-1')

s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION 
)

def download_file_from_s3(bucket, key, local_path):
    s3_client.download_file(bucket, key, local_path)

def load_pickle_file(filepath):
    with open(filepath, 'rb') as f:
        return pickle.load(f)

def load_model():
    local_path = 'model/lightfm_model.pkl'
    download_file_from_s3(S3_BUCKET, 'model/lightfm_model.pkl', local_path)
    return load_pickle_file(local_path)

def load_user_mapping():
    local_path = 'model/user_mapping.pkl'
    download_file_from_s3(S3_BUCKET, 'model/user_mapping.pkl', local_path)
    return load_pickle_file(local_path)

def load_item_mapping():
    local_path = 'model/item_mapping.pkl'
    download_file_from_s3(S3_BUCKET, 'model/item_mapping.pkl', local_path)
    return load_pickle_file(local_path)

def load_item_features():
    local_path = 'model/item_features.pkl'
    download_file_from_s3(S3_BUCKET, 'model/item_features.pkl', local_path)
    return load_pickle_file(local_path)