FROM hashicorp/terraform:latest

RUN apk add --no-cache curl

# add terrafrom modules
ADD . /app
WORKDIR /app
# terraform state directory
RUN mkdir /app/.state
VOLUME .state

WORKDIR /app

RUN terraform init
RUN terraform plan -out=titanic_ml_tfplan_example_3
RUN terraform apply -auto-approve titanic_ml_tfplan_example_3