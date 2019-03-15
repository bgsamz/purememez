import boto3

import config

def get_s3_client():
    if config.INSECURE_S3_ENABLED:
        s3c = boto3.client(
            's3',
            aws_access_key_id=config.ACCESS_KEY,
            aws_secret_access_key=config.SECRET_KEY,
            endpoint_url=config.S3_ENDPOINT,
            verify=False
        )
    else:
        # Else just write to standard s3 with whatever the fuck credentials are on your system
        s3c = boto3.client('s3')
    return s3c

def get(bucket, key):
    s3c = get_s3_client()
    try:
        resp = s3c.get_object(Bucket=bucket, Key=key)
        return resp['Body'].read()
    except e:
        return None


def put_file(bucket, key, filename):
    s3c = get_s3_client()
    try:
        s3c.upload_file(Bucket=bucket, Key=key, Filename=filename)
        return True
    except e:
        return False


def put_stream(bucket, key, bytes_object):
    s3c = get_s3_client()
    try:
        s3c.put_object(Bucket=bucket, Key=key, Body=bytes_object)
        return True
    except e:
        return False
