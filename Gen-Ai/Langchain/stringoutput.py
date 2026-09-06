import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
parser=StrOutputParser()
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.0,
    
    api_key=os.getenv("GROQ_API_KEY")
)

input_prompt=PromptTemplate(template="You are helpful assistent genrate poem about this {person} ", input=["person"])

# input =input_prompt.invoke("sohan")


# output=llm.invoke(input)
# result=parser.invoke(output)

chain=input_prompt | llm | parser
result=chain.invoke("sohan")
print(result) 

