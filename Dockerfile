FROM python:3.9
WORKDIR /FastAPI
COPY /FastAPI/requirements.txt /FastAPI
RUN pip install -r requirements.txt
COPY ./FastAPI /FastAPI
CMD ["uvicorn", "FastAPI.main:app", "--host", "0.0.0.0", "--port", "80"]