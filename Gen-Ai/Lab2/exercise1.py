import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
# College Club Recommendation Chatbot

clubs = {
    "coding": "Coding Club",
    "programming": "Coding Club",
    "java": "Coding Club",
    "python": "Coding Club",
    "web": "Coding Club",
    "technology": "Coding Club",

    "dance": "Dance Club",
    "dancing": "Dance Club",

    "music": "Music Club",
    "singing": "Music Club",
    "guitar": "Music Club",

    "sports": "Sports Club",
    "cricket": "Sports Club",
    "football": "Sports Club",
    "fitness": "Sports Club",

    "art": "Art Club",
    "drawing": "Art Club",
    "painting": "Art Club",

    "photography": "Photography Club",
    "photo": "Photography Club",

    "business": "Entrepreneurship Club",
    "startup": "Entrepreneurship Club",
    "entrepreneurship": "Entrepreneurship Club"
}

print("🎓 College Club Recommendation Chatbot")
print("Type 'exit' to stop.\n")

while True:
    interests = input("Tell me about your interests: ").lower()

    if interests == "exit":
        print("Thank you! Goodbye 👋")
        break

    recommended_club = None
    reason = None

    for keyword, club in clubs.items():
        if keyword in interests:
            recommended_club = club
            reason = f"because you are interested in {keyword}."
            break

    if recommended_club:
        print(f"Recommended Club: {recommended_club}")
        print(f"Reason: {reason}\n")
    else:
        print("Recommended Club: Coding Club")
        print("Reason: It is a good choice for students interested in technology and problem-solving.\n")