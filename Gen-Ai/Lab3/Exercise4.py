# Exercise 4 — Customer Support Reply Generator

# Build a prompt that generates a support reply to a customer message.

# **Input:** `customer_message`, `company_name`, `max_words`

# **Output:** a reply that stays within the word limit, with consistent tone across different inputs

from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API")
)


def translate_sentence(sentence, target_language, formality):

    prompt = f"""
You are a professional multilingual translator.

Translate the given sentence into the requested target language.

Sentence:
{sentence}

Target Language:
{target_language}

Formality Level:
{formality}

Rules:
1. Translate the sentence accurately.
2. Preserve the original meaning.
3. Match the requested formality level.
4. Do not add extra information.
5. Do not explain the translation.
6. Return only the translated sentence.
7. Use proper grammar and natural wording.
8. For Formal, use respectful and professional language.
9. For Informal, use natural and friendly language.
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

    translation = response.choices[0].message.content.strip()

    return translation


while True:

    sentence = input("\nEnter Sentence:\n")

    if sentence.lower() == "exit":
        print("Exiting...")
        break

    target_language = input(
        "Enter Target Language:\n"
    )

    formality = input(
        "Enter Formality (Formal/Informal):\n"
    )

    result = translate_sentence(
        sentence,
        target_language,
        formality
    )

    print("\n========== TRANSLATION ==========\n")
    print(result)