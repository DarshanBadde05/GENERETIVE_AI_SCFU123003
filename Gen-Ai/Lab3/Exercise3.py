from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API")
)

SYSTEM_PROMPT = """
You are a Resume Field Extractor.

Extract only the requested fields from the resume.

Rules:
- Return only valid JSON.
- Return only the requested fields.
- If a field is not found, return null.
- Do not make up information.
- Do not add explanations.
- Keep field names exactly as requested.
"""

while True:

    resume_text = input("\nEnter Resume Text:\n")

    if resume_text.lower() == "exit":
        print("Exiting...")
        break

    fields = input("Enter Fields to Extract:\n")

    prompt = f"""
Resume:
{resume_text}

Fields:
{fields}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    result = response.choices[0].message.content.strip()

    try:
        data = json.loads(result)
        print("\nResult:")
        print(json.dumps(data, indent=4))

    except json.JSONDecodeError:
        print("Invalid JSON.")