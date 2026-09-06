#  Exercise 6 — Recipe to Grocery List Pipeline
# Build a 2-step pipeline. Step 1 extracts ingredients with quantities from a free-form recipe. Step 2 generates a consolidated grocery list scaled to a given number of servings, using only the extracted ingredients from Step 1.
# Input: `recipe\_text`, `target\_servings`
# Output: the extracted ingredient list from Step 1, and the scaled grocery list from Step 2
# Upload to GitHub.

import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.0,
    api_key=os.getenv("GROQ_API_KEY")
)


parser = StrOutputParser()

def extract_ingredients(recipe_text):

    prompt1 = PromptTemplate(
        template="""
You are a recipe analyzer.

Extract:

1. Original number of servings
2. Ingredients
3. Quantity of each ingredient

Recipe:
{recipe_text}
""",
        input_variables=["recipe_text"]
    )

    chain1 = prompt1 | llm | parser

    result = chain1.invoke({
        "recipe_text": recipe_text
    })

    return result

def generate_grocery_list(ingredients, target_servings):

    prompt2 = PromptTemplate(
        template="""
You are a grocery list generator.

Using ONLY the extracted ingredients below,
create a grocery list for {target_servings} servings.

Extracted Ingredients:
{ingredients}

Scale all quantities correctly.

Do not use the original recipe.
""",
        input_variables=[
            "ingredients",
            "target_servings"
        ]
    )

    chain2 = prompt2 | llm | parser

    result = chain2.invoke({
        "ingredients": ingredients,
        "target_servings": target_servings
    })

    return result
def main():

    recipe_text = input("Enter Recipe: ")

    target_servings = input(
        "Enter Target Servings: "
    )
    extracted_ingredients = extract_ingredients(
        recipe_text
    )

    print("\n----- STEP 1 -----")
    print("EXTRACTED INGREDIENTS")
    print(extracted_ingredients)

    grocery_list = generate_grocery_list(
        extracted_ingredients,
        target_servings
    )

    print("\n----- STEP 2 -----")
    print("SCALED GROCERY LIST")
    print(grocery_list)


if __name__ == "__main__":
    main()