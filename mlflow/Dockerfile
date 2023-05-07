FROM python:3.11.3

RUN pip install mlflow
RUN pip install psycopg2==2.9.3

EXPOSE 5000

WORKDIR /server

RUN mkdir /mlflow/