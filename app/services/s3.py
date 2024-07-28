import sys
import time
import boto3
import os
from botocore.exceptions import ClientError
import logging
from boto3.s3.transfer import TransferConfig
from botocore.config import Config
from fastapi import UploadFile

S3_BUCKET = os.getenv('S3_BUCKET')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION', 'eu-north-1')

logger = logging.getLogger('uvicorn')  # Uvicorn'un loggerına bağlanıyoruz
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('upload_log.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))


console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

logger.addHandler(file_handler)
logger.addHandler(console_handler)

s3_config = Config(
    read_timeout=1200,  
    retries={'max_attempts': 2, 'mode': 'standard'} 
)

s3_client = boto3.client(
    's3',
    config=s3_config,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION 
)

def upload_to_s3(file_path, object_name=None):
  
    if object_name is None:
        object_name = os.path.basename(file_path)

    config = TransferConfig(multipart_threshold=1024 * 15,  # 15 MB sınır olsun
                            max_concurrency=10,
                            multipart_chunksize=1024 * 25,  # 15 MB chunk halinde yükelyelim
                            use_threads=True)
    
    file_name = file_path.split('/')[-1]

    total_size = os.path.getsize(file_path)
    uploaded_bytes = 0
    start_time = time.time()

    def callback(bytes_transferred):
        nonlocal uploaded_bytes, start_time  
        current_time = time.time()
        uploaded_bytes += bytes_transferred
        elapsed_time = current_time - start_time
        speed = uploaded_bytes / elapsed_time if elapsed_time > 0 else 0
        remaining_bytes = total_size - uploaded_bytes
        estimated_time = remaining_bytes / speed if speed > 0 else 0
        minutes_remaining = estimated_time / 60
        logger.info(f"{file_name}: Yüklenen: {uploaded_bytes} / {total_size} bytes ({uploaded_bytes / total_size:.2%}), Kalan Süre: {minutes_remaining:.2f} dakika")

    # Dosyanın toplam boyutu
    total_size = os.path.getsize(file_path)
    uploaded_bytes = 0

    try:
        s3_client.upload_file(file_path, S3_BUCKET, object_name,
                              Callback=callback,
                              Config=config)
        logger.info("Yükleme başarıyla tamamlandı!")
        logger.info("-----------------------------")
    except boto3.exceptions.S3UploadFailedError as e:
        logger.error(f"Yükleme başarısız oldu: {e}")
    except Exception as e:
        logger.error(f"Bir hata oluştu: {e}")


def upload_file_object_to_s3(file_object: UploadFile, object_key: str):
  
    try:
        # the file pointer is at the start
        file_object.file.seek(0, os.SEEK_END)
        file_size = file_object.file.tell()
        file_object.file.seek(0)

        uploaded_bytes = 0
        start_time = time.time()

        def callback(bytes_transferred):
            nonlocal uploaded_bytes, start_time
            uploaded_bytes += bytes_transferred
            elapsed_time = time.time() - start_time
            if elapsed_time > 0:
                speed = uploaded_bytes / elapsed_time
                remaining_bytes = file_size - uploaded_bytes
                estimated_time = remaining_bytes / speed if speed > 0 else float('inf')
                minutes_remaining = estimated_time / 60
                logger.info(f"{file_object.filename}: Uploaded {uploaded_bytes / file_size:.2%}, Estimated time remaining: {minutes_remaining:.2f} minutes")

        s3_client = boto3.client('s3')
        s3_client.upload_fileobj(
            file_object.file,
            S3_BUCKET,
            object_key,
            Callback=callback
        )
        logger.info("Upload completed successfully.")
        return object_key
    except Exception as e:
        logger.error(f"An error occurred during S3 upload: {e}")
        raise Exception(f"An error occurred during S3 upload: {str(e)}")


def download_file_from_s3(key, local_path):
 
    if not os.path.exists(os.path.dirname(local_path)):
        os.makedirs(os.path.dirname(local_path))

    try:
       
        response = s3_client.head_object(Bucket=S3_BUCKET, Key=key)
        total_size = int(response['ContentLength'])
        downloaded_bytes = 0

        
        def progress_hook(bytes_transferred):
            nonlocal downloaded_bytes
            downloaded_bytes += bytes_transferred
            percentage = (downloaded_bytes / total_size) * 100
            logger.info(f"Downloading {key}: {downloaded_bytes} of {total_size} bytes ({percentage:.2f}%) completed.")

       
        s3_client.download_file(S3_BUCKET, key, local_path, Callback=progress_hook)
        logger.info("Download completed successfully.")

    except ClientError as e:
        logger.error(f"Error downloading file from S3: {e}")
        raise Exception(f"Error downloading file from S3: {str(e)}")
