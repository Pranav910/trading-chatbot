# from langchain_mistralai import MistralAIEmbeddings
# from langchain_mistralai import MistralAIEmbeddings
# from langchain_community.document_loaders import TextLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_chroma import Chroma
# from langchain.prompts import MessagesPlaceholder, ChatPromptTemplate
# from langchain_core.prompts import MessagesPlaceholder
# from langchain.chains import create_history_aware_retriever
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain_core.output_parsers import StrOutputParser
# from langchain.prompts import ChatPromptTemplate
# from main import llm
# from langchain.chains.retrieval import create_retrieval_chain
# from langchain_core.messages import HumanMessage, AIMessage
# import os


# def load_document(file):
#     loader = TextLoader(os.path.join('../', file))
#     document = loader.load()
#     return document

# documents = load_document('blog.txt')

# text_splitter = RecursiveCharacterTextSplitter(
#     chunk_size=1000,
#     chunk_overlap=200,
#     length_function=len
# )

# splits = text_splitter.split_documents(documents)

# collection_name = "my_collection"
# vectorstore = Chroma(
#     embedding_function=MistralAIEmbeddings(),
#     collection_name=collection_name,
#     persist_directory="./chroma_db"
# )

# vectorstore.add_documents(splits)

# retriever = vectorstore.as_retriever(search_kwargs={"k" : 2})


# contextualize_q_system_prompt = """
# Given a chat history and the latest user question
# which might reference context in the chat history,
# formulate a standalone question which can be understood
# without the chat history. Do NOT answer the question,
# just reformulate it if needed and otherwise return it as is.
# """

# contextualize_q_prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", contextualize_q_system_prompt),
#         MessagesPlaceholder("chat_history"),
#         ("human", "{input}"),
#     ]
# )

# contextualize_chain = contextualize_q_prompt | llm | StrOutputParser()

# history_aware_retriever = create_history_aware_retriever(
#     llm, retriever, contextualize_q_prompt
# )

# qa_prompt = ChatPromptTemplate.from_messages([
#     ("system", "You are a helpful AI assistant. Use the following context to answer the user's question."),
#     ("system", "Context: {context}"),
#     MessagesPlaceholder(variable_name="chat_history"),
#     ("human", "{input}")
# ])

# question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
# rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

# chat_history = []
# question1 = "who is John Doe?"
# answer1 = rag_chain.invoke({"input": question1, "chat_history": chat_history})['answer']
# chat_history.extend([
#     HumanMessage(content=question1),
#     AIMessage(content=answer1)
# ])

# print(f"Human: {question1}")
# print(f"AI: {answer1}\n")

from main import groq_llama

result = groq_llama.invoke("What is the capital of India?")
print(result.content)