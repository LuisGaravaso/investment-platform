#%%
import boto3
from botocore import exceptions
from botocore.exceptions import ClientError
import logging
from dotenv import load_dotenv
from os import getenv

load_dotenv('.awsenv')
ACC_ID = getenv('ACCOUNT_ID')
ACCESS_KEY = getenv('ACCESS_KEY')
ACCESS_SECRET_KEY = getenv('ACCESS_SECRET_KEY')

#%%
s3_client = boto3.client(
    's3',
    aws_access_key_id = ACCESS_KEY,
    aws_secret_access_key = ACCESS_SECRET_KEY
)

#%%
def create_bucket(name:str) -> bool:
    bucket_name = f'{ACC_ID}-{name}'
    try:
        s3_client.create_bucket(Bucket=bucket_name)
        print(f'Successfully created S3 bucket: {bucket_name}')
    except ClientError as e:
        logging.error(e)
        print(f'Failed to create S3 bucket: {bucket_name}')
        return False
    return True

#%%
create_bucket('customers-faker-landing')
create_bucket('customers-faker-athena')
# %%
