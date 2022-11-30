FROM python:3.10

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip3 install -r requirements.txt

COPY . /code

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]

