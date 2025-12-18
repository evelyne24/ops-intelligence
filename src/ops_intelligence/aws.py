import boto3
import os
import logging
from typing import List, Dict

class S3Client:
    def __init__(self):
        self.s3 = boto3.client(
            's3',
            endpoint_url=os.getenv("AWS_ENDPOINT_URL"),
            region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1")
        )
        self.bucket = os.getenv("S3_BUCKET_NAME", "ops-data")
        self.logger = logging.getLogger(__name__)

    def upload_string(self, content: str, object_name: str):
        """Uploads a string directly to S3 as a file."""
        try:
            self.s3.put_object(Bucket=self.bucket, Key=object_name, Body=content)
            self.logger.info(f"✅ Uploaded {object_name} to S3")
        except Exception as e:
            self.logger.error(f"❌ Upload failed: {e}")
            raise

    def list_files(self) -> List[Dict]:
        """Returns a list of files sorted by LastModified (Newest First)."""
        try:
            response = self.s3.list_objects_v2(Bucket=self.bucket)
            if 'Contents' not in response:
                return []
            
            # Sort by date descending
            files = sorted(response['Contents'], key=lambda x: x['LastModified'], reverse=True)
            return files
        except Exception as e:
            self.logger.error(f"❌ List failed: {e}")
            return []

    def download_as_json(self, object_key: str):
        """Downloads file and returns content string."""
        try:
            response = self.s3.get_object(Bucket=self.bucket, Key=object_key)
            return response['Body'].read().decode('utf-8')
        except Exception as e:
            self.logger.error(f"❌ Download failed: {e}")
            raise