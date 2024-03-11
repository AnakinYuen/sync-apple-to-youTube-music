FROM python:3.12.2-slim-bullseye
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src
COPY main.py .
CMD [ "python", "main.py" ]