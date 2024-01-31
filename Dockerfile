FROM python:3.11
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends build-essential libjpeg-dev && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
