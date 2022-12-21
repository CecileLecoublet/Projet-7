FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /FastAPI/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /FastAPI/requirements.txt

COPY ./app /FastAPI/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]