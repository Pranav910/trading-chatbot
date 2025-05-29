from main import llm
from parser import str_output_parser
from prompt_template import prompt, image_prompt, web_search_prompt, query_type_prompt

simple_response_chain = prompt | llm | str_output_parser

image_response_chain = image_prompt | llm |str_output_parser

web_search_response_chain = web_search_prompt | llm | str_output_parser

query_type_response_chain = query_type_prompt | llm | str_output_parser

trading_bot_chain = query_type_prompt | llm | str_output_parser