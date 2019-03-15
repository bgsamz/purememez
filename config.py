import os

# Cough flashblade cough
INSECURE_S3_ENABLED = os.getenv('INSECURE_S3_ENABLED') is not None

ACCESS_KEY = os.getenv('S3_ACCESS_KEY')
print(ACCESS_KEY)

SECRET_KEY = os.getenv('S3_SECRET_KEY')
print(SECRET_KEY)

S3_ENDPOINT = os.getenv('S3_ENDPOINT')
print(S3_ENDPOINT)

MEME_BUCKET = 'memez'
