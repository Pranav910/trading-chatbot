from langchain_community.document_loaders import TextLoader
import os

def load_document(file):
    loader = TextLoader(file)
    document = loader.load()
    return document