import os
from flask import Flask, Response, abort, render_template
import boto3
from botocore.exceptions import ClientError

app = Flask(__name__)

# Configuration
MINIO_URL = os.getenv("MINIO_URL", "http://localhost:9000")
MINIO_BUCKET = os.getenv("MINIO_BUCKET", "videos")
ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin123")

app = Flask(__name__)

# Initialize MinIO S3-compatible client
s3 = boto3.client(
    "s3",
    endpoint_url=MINIO_URL,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
)

@app.route("/getVideos")
def getVideos():
    """
    Returns a plain-text list of all folder names in the bucket.
    """
    PREFIX = ""   # "" = list everything in the bucket. Change to "transcoded/" if needed.

    try:
        print("Starting getVideos request...")
        print(f"Bucket: {MINIO_BUCKET}, Prefix: '{PREFIX}'")
        
        response = s3.list_objects_v2(Bucket=MINIO_BUCKET, Prefix=PREFIX, Delimiter='/')
        
        print(f"Response received. Keys: {response.keys()}")

        folders = []
        
        # Get folders from CommonPrefixes (these are the "directories")
        if "CommonPrefixes" in response:
            print(f"Found {len(response['CommonPrefixes'])} folders")
            for prefix in response["CommonPrefixes"]:
                folder_path = prefix["Prefix"]
                # Remove trailing slash and get folder name
                folder_name = folder_path.rstrip('/').split('/')[-1]
                if folder_name:  # Only add non-empty folder names
                    folders.append(folder_name)
        else:
            print("No CommonPrefixes in response")

        if not folders:
            print("No folders found, returning empty response")
            return Response("No folders found.", mimetype="text/plain")

        print(f"Returning {len(folders)} folders")
        return Response("\n".join(folders), mimetype="text/plain")

    except ClientError as e:
        print("MinIO ClientError:", e)
        abort(500)
    except Exception as e:
        print("Unexpected error:", type(e).__name__, str(e))
        abort(500)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/legal")
def legal():
    return render_template("legal.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/team")
def team():
    return render_template("team.html")

@app.route("/videos")
def videos():
    return render_template("videos.html")

if __name__ == "__main__":
    app.run(debug=True, port=3000)
