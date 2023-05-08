FROM library/postgres:9.6-alpine

COPY create-multiple-postgres-db.sh /docker-entrypoint-initdb.d/

RUN chmod +x /docker-entrypoint-initdb.d/create-multiple-postgres-db.sh

EXPOSE 5432