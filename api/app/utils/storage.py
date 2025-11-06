

import boto3
from ..config import settings

def s3_client():
    return boto3.client(
        "s3",
        endpoint_url=settings.minio_endpoint_url,
        aws_access_key_id=settings.minio_access_key,
        aws_secret_access_key=settings.minio_secret_key,
        region_name=settings.minio_region,
    )

def put_object(key: str, data: bytes, content_type: str):
    s3 = s3_client()
    try:
        s3.head_bucket(Bucket=settings.minio_bucket)
    except:
        s3.create_bucket(Bucket=settings.minio_bucket)
    s3.put_object(Bucket=settings.minio_bucket, Key=key, Body=data, ContentType=content_type)
