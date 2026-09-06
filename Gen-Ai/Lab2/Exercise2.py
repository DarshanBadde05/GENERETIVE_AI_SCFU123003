# Exercise 2 — Content Generator
# Build an app that generates Instagram captions for a college fest.
# Required functionality:
# Accepts two inputs: fest name and fest theme
# Generates exactly 3 caption options, each under 30 words
# Each caption includes at least one relevant hashtag
# Upload to GitHub.

import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_captions(fest_name, fest_theme):

    prompt = f"""
Generate exactly 3 Instagram captions for a college fest.

Fest Name: {fest_name}
Fest Theme: {fest_theme}

Rules:
1. Generate exactly 3 captions.
2. Each caption must be under 30 words.
3. Each caption must contain at least one relevant hashtag.
4. Make captions attractive and fun.
5. Number the captions 1, 2, and 3.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7
    )

    return response.choices[0].message.content.strip()


fest_name = input("Enter Fest Name: ")
fest_theme = input("Enter Fest Theme: ")

result = generate_captions(
    fest_name,
    fest_theme
)

print("\n===== INSTAGRAM CAPTIONS =====")
print(result)