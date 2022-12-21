FROM python:3.9

RUN pip install fastapi uvicorn

EXPOSE 8000

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]