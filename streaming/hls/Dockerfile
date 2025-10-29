# Use a lightweight Python runtime
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy dependencies file (optional if you want requirements.txt)
# Copy Python code
COPY stream.py /app/

# Install required packages
RUN pip install flask boto3

# Expose port (Flask runs on 8081)
EXPOSE 8081

# Run streaming server
CMD ["python", "stream.py"]
