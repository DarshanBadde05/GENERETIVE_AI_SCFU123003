import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# Patient input
patient_name = input("Enter patient name: ")
patient_notes = input("Enter patient consultation notes: ")

# Prompt
PROMPT = f"""
You are a medical documentation assistant.

Convert the patient's raw consultation notes into a clean,
concise doctor's summary.

Patient Name: {patient_name}

Patient Notes:
{patient_notes}

Rules:
1. Use only the information provided in the notes.
2. Do not invent symptoms, diagnoses, medicines, or treatments.
3. Use clear and professional language.
4. Always use exactly these three sections:
   Symptoms
   Diagnosis
   Recommendation
5. If information is missing, write:
   "Not provided in the consultation notes."
6. Do not add any extra sections.

Output format:

Patient Name: {patient_name}

Symptoms
- ...

 Diagnosis
...

Recommendation
- ...
"""

response = client.chat.completions.create(
  model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "user",
            "content": PROMPT
        }
    ],
    temperature=0.2
)

print("\n========== DOCTOR SUMMARY ==========\n")
print(response.choices[0].message.content)


# Patient complains of cough, sore throat and mild fever for three days.
# Doctor suspects a common viral respiratory infection and recommended
# rest, warm fluids and monitoring the fever.