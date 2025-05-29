FROM python

WORKDIR /chatapi

COPY /requirements.txt /chatapi/

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY /fast_chat_api /chatapi/

EXPOSE 8000

CMD [ "fastapi", "run", "api.py" ]