import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

review_text = input("Enter customer review: ")

prompt = f""" You are a customer review classifier. Your task is to classify the following customer review into exactly ONE category.
Categories: 
        POSITIVE: The customer is happy or satisfied with the product or service.
        NEGATIVE: The customer is unhappy, dissatisfied, or complaining about the product or service. 
        NEUTRAL: The review gives factual information without a clear positive or negative opinion.
        MIXED: The review contains both positive and negative opinions. 
Rules: 
        1. Read the customer review carefully. 
        2. Select only ONE category. 
        3. Return ONLY the category name.
        4. Do not give any explanation. 
        5. Do not use punctuation. 
        6. The output must be exactly one of: POSITIVE NEGATIVE NEUTRAL MIXED Customer Review: {review_text} """

response = client.chat.completions.create( 
        model="openai/gpt-oss-20b",
        messages=[ { "role": "user", "content": prompt } ], 
        temperature=0.2 )

category = response.choices[0].message.content.strip()
print("\nCategory:", category)
