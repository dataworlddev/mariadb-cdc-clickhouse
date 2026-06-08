# mariadb-cdc-clickhouse

## useful commands

### build consumer
docker compose up -d --build --force-recreate consumer

### check if kafka topics created after running debezium command
docker exec -it mariadb-cdc-clickhouse-kafka-1 kafka-topics \
--bootstrap-server localhost:9092 \
--list
### see topics data in kafka
docker exec -it mariadb-cdc-clickhouse-kafka-1 kafka-console-consumer \
--bootstrap-server localhost:9092 \
--topic app.app_db.users \
--from-beginning