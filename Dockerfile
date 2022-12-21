FROM python:3.9

WORKDIR /FastAPI

COPY FastAPI/requirements.txt /FastAPI/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /FastAPI/requirements.txt

COPY ./FastAPI ./FastAPI

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]