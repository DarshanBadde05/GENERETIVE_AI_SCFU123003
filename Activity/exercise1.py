import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

PROMPT = """
You are a College Club Recommendation Chatbot.

Ask the student about their interests, hobbies and skills.
Based on their answer, recommend the best college club.

Available clubs:
- AI/ML Club
- Coding Club
- Web Development Club
- Robotics/IoT Club
- Cybersecurity Club
- Entrepreneurship Club
- Sports Club
- Photography/Media Club
- Music/Dance Club
- Art/Design Club
- Literary/Debate Club

Give:
1. Best club
2. Match percentage
3. Short reason
4. Two other suitable clubs

Keep the answer short and friendly.
"""

history = [{"role": "system", "content": PROMPT}]

print("College Club Recommendation Chatbot")
print("Type 'exit' to quit.\n")

while True:
    user = input("Student: ")

    if user.lower() == "exit":
        print("Thank you! ")
        break

    history.append({
        "role": "user",
        "content": user
    })

    response = client.chat.completions.create(
        messages=history,
        model="openai/gpt-oss-20b"
    )

    answer = response.choices[0].message.content

    history.append({
        "role": "assistant",
        "content": answer
    })

    print("\nchatbot:", answer)