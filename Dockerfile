FROM python:3.9

RUN pip install fastapi uvicorn

EXPOSE 80

COPY ./FastAPI /FastAPI

CMD ["uvicorn", "FastAPI.main:app", "--host", "0.0.0.0", "--port", "80"]