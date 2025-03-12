FROM python:3.10

WORKDIR /project

COPY ./requirements.txt .

RUN apt-get update

RUN pip install --upgrade pip &&\
    pip install -r requirements.txt

COPY . .

ENTRYPOINT [ "python", "main.py"] 