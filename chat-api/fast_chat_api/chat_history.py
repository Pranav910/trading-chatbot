from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from chain import simple_response_chain, image_response_chain, web_search_response_chain

store = {}

def get_session_history(session_id : str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


with_chat_history = RunnableWithMessageHistory(simple_response_chain, get_session_history)

with_chat_history_with_image = RunnableWithMessageHistory(image_response_chain, get_session_history)

with_web_search_chat_history = RunnableWithMessageHistory(web_search_response_chain, get_session_history)