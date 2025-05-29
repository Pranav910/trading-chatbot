from chain import query_type_response_chain

def get_query_type(query):
    
    query_type = query_type_response_chain.invoke({'query': query})

    return query_type