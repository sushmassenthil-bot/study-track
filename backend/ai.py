from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()


def generate_study_advice(prompt: str):
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
    )

    return response.text