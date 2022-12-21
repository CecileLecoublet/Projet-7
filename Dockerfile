FROM python:3.9

RUN mkdir /FastAPI

WORKDIR /FastAPI

COPY /FastAPI/requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "FastAPI.main:app", "--host=0.0.0.0", "--port=80"]