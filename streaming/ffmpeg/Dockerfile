# 1. Use lightweight base image that supports ffmpeg
FROM python:3.11-slim

# 2. Install ffmpeg (required for transcoding)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# 3. Create working directory
WORKDIR /app

# 4. Copy requirements and install python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy rest of application code
COPY transcode.py .

# # Environment vars (change later as needed)
# ENV MINIO_URL=http://minio:9000
# ENV MINIO_BUCKET=videos
# ENV MINIO_ACCESS_KEY=minioadmin
# ENV MINIO_SECRET_KEY=minioadmin123

# 6. Expose Flask port
EXPOSE 8080

# 7. Run your Flask app
CMD ["python", "transcode.py"]
