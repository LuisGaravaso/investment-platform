#%%
import boto3
from botocore import exceptions
from botocore.exceptions import ClientError
import logging
from dotenv import load_dotenv
import os

load_dotenv('.awsenv')
ACC_ID = os.getenv('ACCOUNT_ID')
ACCESS_KEY = os.getenv('ACCESS_KEY')
ACCESS_SECRET_KEY = os.getenv('ACCESS_SECRET_KEY')

#%%
s3_client = boto3.client(
    's3',
    aws_access_key_id = ACCESS_KEY,
    aws_secret_access_key = ACCESS_SECRET_KEY
)

#%%
def create_bucket(name:str) -> tuple:
    
    bucket_name = f'{ACC_ID}-{name}'
    
    try:
        s3_client.create_bucket(Bucket=bucket_name)
        print(f'Successfully created S3 bucket: {bucket_name}')
        
    except ClientError as e:
        logging.error(e)
        print(f'Failed to create S3 bucket: {bucket_name}')
        return bucket_name, False
    
    return bucket_name, True

#%%
def upload_file(filename, bucket, subfolders = None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    # If S3 object_name was not specified, use file_name
    if subfolders is None:
        subfolders = os.path.basename(filename)
    else:
        subfolders = f'{subfolders}/{filename}'
    try:
        response = s3_client.upload_file(filename, bucket, subfolders)
    except ClientError as e:
        logging.error(e)
        return False
    return True