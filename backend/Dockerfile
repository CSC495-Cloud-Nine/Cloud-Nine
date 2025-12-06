FROM python:3.11-slim

WORKDIR /app

# Copy only requirements first (for build caching)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend directory contents
COPY . .

# Expose your server port (update if needed)
EXPOSE 3000

CMD ["python", "server.py"]
