FROM python:3.9

RUN pip install fastapi uvicorn

EXPOSE 5000

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]