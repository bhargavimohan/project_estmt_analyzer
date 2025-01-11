#  Python image 
FROM python:3.12-bullseye
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src ./src
COPY DB ./DB
EXPOSE 8002
WORKDIR /app/src

CMD ["uvicorn", "server:app", "--host", "0.0.0.0","--port", "8002"]