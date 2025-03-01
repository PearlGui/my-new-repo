import os
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def main():
    # 1. Initialize LLM (OpenAI in this example)
    # Make sure you have an environment variable OPENAI_API_KEY set
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        print("Error: OPENAI_API_KEY not set. Please set it in your environment.")
        return
    
   llm = OpenAI(
    temperature=0.7,
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    model_name="text-davinci-003"
   )

    # 2. Create a prompt template
    prompt = PromptTemplate(
        input_variables=["topic"],
        template="You are a helpful research assistant. Provide a concise overview about {topic}."
    )

    # 3. Create an LLM chain
    chain = LLMChain(llm=llm, prompt=prompt)

    # 4. Ask the user for a topic
    user_topic = input("What topic do you want to research? ")

    # 5. Run the chain with the user's topic
    response = chain.run(topic=user_topic)

    # 6. Print the result
    print("\n=== Research Summary ===")
    print(response)

if __name__ == "__main__":
    main()

from langchain.llms import Ollama

llm = Ollama(model="llama2", system_prompt="You are a helpful research assistant.")

