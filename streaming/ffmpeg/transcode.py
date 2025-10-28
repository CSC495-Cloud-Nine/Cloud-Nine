# docker run -p 9000:9000 -p 9001:9001 -e MINIO_ROOT_USER=minioadmin -e MINIO_ROOT_PASSWORD=minioadmin123 minio/minio server /data --console-address ":9001"

import os
import subprocess
import boto3
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import tempfile

# Configuration
MINIO_URL = os.getenv("MINIO_URL", "http://localhost:9000")
MINIO_BUCKET = os.getenv("MINIO_BUCKET", "videos")
ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin123")

# Initialize Flask app
app = Flask(__name__)

# Initialize S3 client (MinIO)
s3 = boto3.client(
    "s3",
    endpoint_url=MINIO_URL,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
)

@app.route("/upload", methods=["POST"])
def upload_and_transcode():
    """Upload a video, transcode it to HLS, and upload to MinIO."""
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    
    # Temporary input and output directories
    with tempfile.TemporaryDirectory() as temp_dir:
        input_path = os.path.join(temp_dir, filename)
        output_dir = os.path.join(temp_dir, "output")
        os.makedirs(output_dir, exist_ok=True)

        # Save the uploaded file
        file.save(input_path)

        # Transcode using ffmpeg to HLS
        output_m3u8 = os.path.join(output_dir, "index.m3u8")
        cmd = [
            "ffmpeg", "-i", input_path,
            "-codec:", "copy",
            "-start_number", "0",
            "-hls_time", "10",
            "-hls_list_size", "0",
            "-f", "hls", output_m3u8
        ]
        subprocess.run(cmd, check=True)

        # Upload HLS files to MinIO
        uploaded_files = []
        for root, _, files in os.walk(output_dir):
            for f in files:
                full_path = os.path.join(root, f)
                s3_key = f"{os.path.splitext(filename)[0]}/{f}"
                s3.upload_file(full_path, MINIO_BUCKET, s3_key)
                uploaded_files.append(f"{MINIO_URL}/{MINIO_BUCKET}/{s3_key}")

        return jsonify({
            "message": "Transcoding and upload complete.",
            "files": uploaded_files
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
