import os
import json
import time
import boto3
import requests
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST")
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
DATE = os.getenv("DATE", "2025-04-29")
LEAGUE_NAME = os.getenv("LEAGUE_NAME", "NCAA")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")
LIMIT = int(os.getenv("LIMIT", 10))

INPUT_KEY = "highlights/basketball_highlights.json"  
OUTPUT_KEY = "videos/highlight.mp4"                  

WAIT_TIME_BETWEEN_STEPS = 10


# get highlights from API
def fetch_highlights():
    try:
        query_params = {"date": DATE, "leagueName": LEAGUE_NAME, "limit": LIMIT}
        headers = {"X-RapidAPI-Key": RAPIDAPI_KEY, "X-RapidAPI-Host": RAPIDAPI_HOST}

        response = requests.get(API_URL, headers=headers, params=query_params)
        response.raise_for_status()
        highlights = response.json()

        print("api_url:", API_URL)
        print("Highlights fetched successfully!")
        return highlights
    except Exception as e:
        print(f"Error fetching highlights: {e}")
        return None


# save highlights JSON to S3
def save_to_s3(data, file_name):
    try:
        s3 = boto3.client("s3", region_name=AWS_REGION)

        s3_key = f"highlights/{file_name}.json"
        s3.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=s3_key,
            Body=json.dumps(data),
            ContentType="application/json"
        )
        print(f"Highlights saved: s3://{S3_BUCKET_NAME}/{s3_key}")
        return s3_key
    except Exception as e:
        print(f"Error saving highlights: {e}")
        return None

# process one video from highlights and upload to S3
def process_one_video(input_key=INPUT_KEY, output_key=OUTPUT_KEY):
    try:
        s3 = boto3.client("s3", region_name=AWS_REGION)

        print("Fetching highlights JSON from S3...")
        response = s3.get_object(Bucket=S3_BUCKET_NAME, Key=input_key)
        highlights = json.loads(response["Body"].read().decode("utf-8"))

        # Check if "data" exists and has items
        if not highlights.get("data"):
            print("No video highlights found in the JSON file.")
            return

        video_url = highlights["data"][0].get("url")
        if not video_url:
            print("No video URL found in the first highlight.")
            return

        print(f"Processing video URL: {video_url}")

        video_response = requests.get(video_url, stream=True)
        video_response.raise_for_status()
        video_data = BytesIO(video_response.content)

        s3.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=output_key,
            Body=video_data,
            ContentType="video/mp4"
        )
        print(f"Video uploaded: s3://{S3_BUCKET_NAME}/{output_key}")
    except Exception as e:
        print(f"Error during video processing: {e}")


# run the pipeline once (no infinite loop)
def run_pipeline():
    try:
        print("Starting pipeline...")

        highlights = fetch_highlights()
        if highlights:
            input_key = save_to_s3(highlights, "basketball_highlights")

            if input_key:  # only continue if highlights were saved
                print("Waiting before video processing...")
                time.sleep(WAIT_TIME_BETWEEN_STEPS)

                process_one_video(input_key)

        print("Pipeline completed!")
    except Exception as e:
        print(f"Pipeline error: {e}")


# call the main function
if __name__ == "__main__":
    run_pipeline()
