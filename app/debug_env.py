from dotenv import load_dotenv
import os

load_dotenv()

print("API_URL:", os.getenv("API_URL"))
print("RAPIDAPI_KEY:", os.getenv("RAPIDAPI_KEY"))
print("RAPIDAPI_HOST:", os.getenv("RAPIDAPI_HOST"))

