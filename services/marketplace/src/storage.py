from src.config import settings

from src.services.storage import S3Provider

import boto3

s3_client = boto3.client(
    "s3",
    endpoint_url=settings.ENDPOINT_URL,
    region_name=settings.REGION_NAME,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
)

s3_provider = S3Provider(s3_client)



