import os
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def main():
    # 1. Initialize LLM (OpenAI or Ollama)
    llm = OpenAI(
        temperature=0.7,
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        model_name="text-davinci-003"  # or "gpt-3.5-turbo" if using ChatCompletion
    )

    # 2. Create a prompt template
    prompt = PromptTemplate(
        input_variables=["topic"],
        template="You are a helpful research assistant. Provide a concise overview about {topic}."
    )

    # 3. Create an LLM chain
    chain = LLMChain(llm=llm, prompt=prompt)

    # 4. Ask the user for a topic and run the chain
    user_topic = input("What topic do you want to research? ")
    response = chain.run(topic=user_topic)
    print("\n=== Research Summary ===")
    print(response)

if __name__ == "__main__":
    main()
