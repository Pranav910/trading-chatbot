from langchain_mistralai import ChatMistralAI
from groq import Groq
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv()

# llm = ChatMistralAI(
#     model_name="mistral-large-latest",
#     temperature=0.5,
#     max_retries=2
# )

llm = init_chat_model("meta-llama/llama-4-scout-17b-16e-instruct", model_provider="groq")

groq_llama = init_chat_model("llama3-8b-8192", model_provider="groq")