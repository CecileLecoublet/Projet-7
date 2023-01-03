FROM python:3.9

RUN pip install fastapi uvicorn pandas

EXPOSE 8000

COPY ./FastAPI /FastAPI

CMD ["uvicorn", "FastAPI.main:app", "--host=0.0.0.0" , "--reload" , "--port", "8000"]