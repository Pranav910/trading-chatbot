import asyncio
from crawler import crawl, load_results_concurrently
from generate_image_response import generate_ocr_response
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from allowed_origins import origins
from generate_response import generate_response
from pydantic import BaseModel
from get_query_type import get_query_type
from get_train_status import get_train_status
from rag_response_generator import generate_rag_response
import os
import shutil

class Item(BaseModel):
    type : str
    prompt : str | None = None

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def root():
    return "this is root route"

@app.post("/api/v1/response")
def send_model_response(item : Item):
    result = generate_response(item.prompt, 'without_image')
    # print(f"result : {result}")
    return {'result' : result}

@app.post("/api/v1/file_response")
def send_model_response_with_file(file : UploadFile = File(...), user_prompt : str = Form()):
    file_path = os.path.join('./', file.filename)
    if os.path.exists(file_path) == False:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    respone = generate_rag_response(file_path, user_prompt)
    
    return {'result' : respone}


@app.post("/api/v1/image_response")
async def send_model_response_with_image(file : UploadFile = File(...), user_prompt : str = Form()):
    image_file_path = os.path.join('./', file.filename)

    with open(image_file_path, 'wb') as image_buffer:
        shutil.copyfileobj(file.file, image_buffer)
        
    ocr_response = generate_ocr_response(image_file_path)

    # print(f"OCR Response : {ocr_response}")

    result = generate_response(ocr_response, 'with_image')

    return {'result' : result}

@app.post("/api/v1/get_web_search_results")
def crawlWeb(item: Item):

    query = item.prompt

    # query_type = get_query_type(query)

    urls, favicon_links = crawl(query)

    # if query_type == "train":
    #     result = asyncio.run(get_train_status(urls))
    # else:
    result = load_results_concurrently(urls)

    content = ""

    for data in result:
        content += data + " \n "

    result = generate_response(content, query, 'with_web_search')

    return {'result': result, 'sources': favicon_links}