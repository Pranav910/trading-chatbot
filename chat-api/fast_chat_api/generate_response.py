from chat_history import with_chat_history, with_chat_history_with_image, with_web_search_chat_history
from langchain_core.messages import HumanMessage
from model_config import config
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_mistralai import MistralAIEmbeddings
from langchain.vectorstores import FAISS


def generate_response(prompt, alternate_prompt, prompt_type='without_image'):

    if prompt_type == 'without_image':
        # print("with chat history : ", with_chat_history.get_prompts(config=config))
        result = with_chat_history.invoke(
            [HumanMessage(content=prompt)],
            config=config
        )
        return result
    
    elif prompt_type == 'with_image':
        result = with_chat_history_with_image.invoke(
            [HumanMessage(content=prompt)],
            config=config
        )
        return result

    elif prompt_type == "with_web_search":

        # text_splitter = RecursiveCharacterTextSplitter(
        #     chunk_size=300,
        #     chunk_overlap=10,
        #     unction=len
        # )

        # splits = text_splitter.split_documents([Document(page_content=prompt)])

        # vectore_store = FAISS.from_documents(splits, MistralAIEmbeddings())

        # results = vectore_store.similarity_search(query=alternate_prompt, k=10)

        # content = ""

        # for data in results:
        #     content = content + data.page_content + "\n\n"

        final_prompt = f"""user_prompt: {alternate_prompt}
        prompt_answer: {prompt[:32000]}
        """

        result = with_web_search_chat_history.invoke(
            [HumanMessage(content=final_prompt)],
            config=config
        )

        return result