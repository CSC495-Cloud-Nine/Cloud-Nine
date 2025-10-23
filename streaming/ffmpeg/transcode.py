import os
import subprocess
import boto3

MINIO_URL = os.getenv("MINIO_URL", "http://localhost:9000") # Change localhost to the ip address of the minio deployment
MINIO_BUCKET = os.getenv("MINIO_BUCKET", "videos")
ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin123")

# Path setup
input_file = r"C:\Users\jeffr\Videos\Screen Recordings\Customer Portal.mp4"
output_dir = "/output"

os.makedirs(output_dir, exist_ok=True)

# Transcode to HLS
subprocess.run([
    "ffmpeg", "-i", input_file,
    "-codec:", "copy",
    "-start_number", "0",
    "-hls_time", "10",
    "-hls_list_size", "0",
    "-f", "hls", f"{output_dir}/index.m3u8"
], check=True)

# Upload to MinIO
s3 = boto3.client("s3",
                  endpoint_url=MINIO_URL,
                  aws_access_key_id=ACCESS_KEY,
                  aws_secret_access_key=SECRET_KEY)

for root, _, files in os.walk(output_dir):
    for f in files:
        full_path = os.path.join(root, f)
        s3.upload_file(full_path, MINIO_BUCKET, f)
        print(f"Uploaded {f} to MinIO bucket {MINIO_BUCKET}")