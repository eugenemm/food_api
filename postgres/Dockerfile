FROM postgres:9.6

ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_HOST_AUTH_METHOD=trust

COPY ./init-db.sh /docker-entrypoint-initdb.d

#RUN psql -d postgres -c "CREATE USER food_backend_db_user WITH PASSWORD '12345678';"

#RUN psql -d postgres -c "CREATE DATABASE food_db  OWNER 'food_backend_db_user';"

EXPOSE 5432
