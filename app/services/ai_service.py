from openai import OpenAI
from app.config import settings
from app.prompts.resume_prompt import generate_prompt

def generate_resume(github_data):
    client = OpenAI(api_key=settings.openai_api_key)
    prompt = generate_prompt(github_data)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
    