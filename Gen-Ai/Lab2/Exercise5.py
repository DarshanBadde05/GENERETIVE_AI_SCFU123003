# Exercise 5 — AI Tutor
# Build an app that tutors a first-year student on one topic.
# Required functionality:
# Accepts a topic name and gives an initial explanation
# Detects when the user says something like "I don't get it" and re-explains differently
# Tracks how many times it has re-explained the same topic in the session
# Runs in a loop until the user says they understand or exits
# Upload to GitHub.

import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def explain_topic(topic, re_explain=False):

    if re_explain:

        instruction = """
Explain the topic again in a simpler and
different way with a real-world example.
"""

    else:

        instruction = """
Explain the topic simply for a first-year
college student.
"""

    prompt = f"""
You are an AI tutor.

Topic:
{topic}

{instruction}

Use simple language.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.4
    )

    return response.choices[0].message.content.strip()


# Get topic
topic = input("Enter Topic: ")

# Counter
re_explain_count = 0


# Initial explanation

print("\n===== EXPLANATION =====")

result = explain_topic(topic)

print(result)


# Loop

while True:

    user_response = input(
        "\nDo you understand? "
        "(yes / no / exit): "
    ).lower()


    if user_response == "yes":

        print(
            "\nGreat! You understood the topic."
        )

        print(
            "Re-explained:",
            re_explain_count,
            "time(s)"
        )

        break


    elif user_response == "no":

        re_explain_count += 1

        print(
            f"\n===== RE-EXPLANATION "
            f"{re_explain_count} ====="
        )

        result = explain_topic(
            topic,
            re_explain=True
        )

        print(result)


    elif user_response == "exit":

        print("\nThank you! Goodbye ")

        break


    else:

        print(
            "Please enter yes, no, or exit."
        )