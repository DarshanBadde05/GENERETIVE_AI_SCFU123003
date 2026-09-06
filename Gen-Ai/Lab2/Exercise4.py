# Exercise 4 — Document Summarizer
# Build an app that summarizes a research paper abstract at two levels.
# Required functionality:
# Accepts one block of text as input
# Produces a 2-line summary and a separate 5-line summary from that single input, in one run
# Upload to GitHub.

import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def summarize_document(text):

    prompt = f"""
You are a research paper summarizer.

Summarize the following research paper abstract
at two different levels.

Text:
{text}

Return exactly in this format:

2-LINE SUMMARY:
Write exactly 2 lines.

5-LINE SUMMARY:
Write exactly 5 lines.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content.strip()


text = input("Enter Research Paper Abstract: ")

result = summarize_document(text)

print("\n===== SUMMARY =====")
print(result)