import boto3
import os

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket_name = 'your-bucket-name'
    file_path = '/path/to/your/file.pdf'
    s3_key = 'uploaded/file.pdf'

    try:
        with open(file_path, 'rb') as file:
            s3.upload_fileobj(file, bucket_name, s3_key)
        return {
            'statusCode': 200,
            'body': 'File uploaded successfully'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }