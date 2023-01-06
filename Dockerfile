FROM python:3.9

COPY requirements.txt /requirements.txt

RUN pip install -r requirements.txt

EXPOSE 80

COPY ./FastAPI /FastAPI

CMD ["uvicorn", "main:app", "--host=0.0.0.0" , "--reload" , "--port", "80"]