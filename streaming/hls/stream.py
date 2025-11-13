import os
from flask import Flask, Response, abort
import boto3
from botocore.exceptions import ClientError

# Configuration
MINIO_URL = os.getenv("MINIO_URL", "http://minio:9000")
MINIO_BUCKET = os.getenv("MINIO_BUCKET", "videos")
ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin123")

app = Flask(__name__)

# Initialize MinIO S3 client
s3 = boto3.client(
    "s3",
    endpoint_url=MINIO_URL,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
)

@app.route("/stream/<video>/<path:filename>")
def stream(video, filename):
    """
    Stream HLS video files (.m3u8 or .ts) from MinIO.
    Example:
        http://localhost:8081/stream/myvideo/index.m3u8
        http://localhost:8081/stream/myvideo/segment0.ts
    """
    key = f"{video}/{filename}"

    try:
        minio_object = s3.get_object(Bucket=MINIO_BUCKET, Key=key)
        data = minio_object["Body"].read()

        # Determine correct content type
        content_type = (
            "application/vnd.apple.mpegurl" if filename.endswith(".m3u8")
            else "video/mp2t"
        )

        return Response(data, mimetype=content_type)

    except ClientError as e:
        print("MinIO Error:", e)
        abort(404)

@app.route("/")
def root():
    return """
    <h2>🎬 HLS Video Streaming Server</h2>
    <p>Use the following format to stream a video:</p>
    <code>http://localhost:8081/stream/VIDEO_NAME/index.m3u8</code>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
