docker exec -it mariadb-cdc-clickhouse-kafka-1 kafka-topics \
--bootstrap-server localhost:9092 \
--list

# expected output: 
# __consumer_offsets
# app
# app.app_db.orders
# app.app_db.users
# connect_configs
# connect_offsets
# connect_statuses
# schemahistory.app_db

# docker compose up -d --build --force-recreate consumer