import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from pydantic import BaseModel, Field

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.0,
    api_key=os.getenv("GROQ_API_KEY")
)

class Review(BaseModel):

    complaint: str = Field(description="Core complaint of the customer")
    product_or_feature: str = Field(description="Product or feature mentioned")
    sentiment: str = Field(description="Customer sentiment")

parser = PydanticOutputParser(pydantic_object=Review)

input_prompt = PromptTemplate(
    template="""  complaint ,Product or feature and Customer sentiment{review_text}  {format_instructions}""",

    input_variables=["review_text"],

    partial_variables={
        "format_instructions": parser.get_format_instructions()
        
    }
)
chain1 = input_prompt | llm | parser

ticket_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a professional support ticket writer."
    ),
    (
        "human",
        """

Complaint: {complaint}

Product/Feature: {product_or_feature}

Sentiment: {sentiment}

Write the ticket in this format:

Issue:
Product/Feature:
Sentiment:
Suggested Action:
"""
    )
])

parser2 = StrOutputParser()

chain2 = ticket_prompt | llm | parser2


review_text = input("Enter customer review: ")
result1 = chain1.invoke({
    "review_text": review_text
})

print("\n--- STEP 1 OUTPUT ---")

print("Complaint:", result1.complaint)
print("Product/Feature:", result1.product_or_feature)
print("Sentiment:", result1.sentiment)

result2 = chain2.invoke({
    "complaint": result1.complaint,
    "product_or_feature": result1.product_or_feature,
    "sentiment": result1.sentiment
})


print("\n--- STEP 2 SUPPORT TICKET ---")

print(result2) 