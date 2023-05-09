FROM python:3.9.13

RUN pip install mlflow
RUN pip install psycopg2==2.9.3

EXPOSE 5000

RUN mkdir -p /server

WORKDIR /server
COPY . /server

RUN mkdir ./mlflow
RUN chmod 777 ./mlflow

CMD ["mlflow", "server", "--backend-store-uri", "postgresql://mlflow:mlflow@postgres:5432/mlflow", "--default-artifact-root", "wasbs://contentestml@storacctestml.blob.core.windows.net/arts", "--host", "0.0.0.0" ]