from langchain_chroma import Chroma
from langchain_mistralai import MistralAIEmbeddings
from document_loader import load_document
from text_splitter import text_splitter
from langchain_core.messages import AIMessage, HumanMessage
from langchain.chains import create_history_aware_retriever
from main import groq_llama as llm
from contextualize_chain import contextualize_q_prompt
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain

rag_chat_history = []

def generate_rag_response(file, user_prompt):

    documents = load_document(file)
    splits = text_splitter.split_documents(documents)
    collection_name = "my_collection"
    vectorstore = Chroma(
        embedding_function=MistralAIEmbeddings(),
        collection_name=collection_name,
        persist_directory="./chroma_db"
    )
    vectorstore.add_documents(splits)
    retriever = vectorstore.as_retriever(search_kwargs={"k" : 2})

    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )

    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful AI assistant. Use the following context to answer the user's question."),
        ("system", "Context: {context}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ])

    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    answer = rag_chain.invoke({"input": user_prompt, "chat_history": rag_chat_history})['answer']

    rag_chat_history.extend([
        HumanMessage(content=user_prompt),
        AIMessage(content=answer)
    ])

    return answer

# answer = generate_rag_response('blog.txt', 'What is John Doe used to refer?')

# print(answer)