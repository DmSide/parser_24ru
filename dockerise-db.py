# docker run -p 5432:5432 -d \
# -e POSTGRES_USER="objectrocket" \
# -e POSTGRES_PASSWORD="1234" \
# -e POSTGRES_DB="some_db" \
# -v ${PWD}/pg-data:/var/lib/postgresql/data \
# --name pg-container \
# postgres