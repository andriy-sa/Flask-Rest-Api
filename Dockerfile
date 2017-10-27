FROM python:3.5.4-slim
WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install htop
RUN apt-get install -y build-essential libpq-dev git libsqlite3-dev
RUN pip install -r requirements.txt

CMD ["python","run.py"]