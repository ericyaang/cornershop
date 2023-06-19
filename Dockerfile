FROM python:3.11

WORKDIR /cornershop

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./src ./src

CMD ["python", "./src/get_json.py"]