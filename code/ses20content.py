from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file
client = OpenAI()

topic = input("Enter a story topic: ").strip()
if not topic:
    topic = "a unicorn"

response = client.responses.create(
    model = "gpt-3.5-turbo",
    inputs = [
        {"role": "system", "content": "You are a helpful assistant that writes creative stories."},
        {"role": "user", "content": f"Write a short story about {topic}."}
    ]  
)

print(response.output_text)

