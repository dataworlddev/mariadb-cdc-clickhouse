import json
import os
from dotenv import load_dotenv
from confluent_kafka import Consumer
from handlers.users import process_users
from handlers.orders import process_orders

load_dotenv()  

print ("start consuming process!")
TOPIC_HANDLERS = {
    "app.app_db.users": process_users,
    "app.app_db.orders": process_orders,
}

consumer = Consumer({
    "bootstrap.servers": "kafka:9092",
    "group.id": "cdc-consumer-try1",
    "enable.auto.commit": False,
    "auto.offset.reset": "earliest"
})

consumer.subscribe(list(TOPIC_HANDLERS.keys()))

print("CDC Consumer started...")

while True:
    msg = consumer.poll(1.0)

    if msg is None:
        continue

    if msg.error():
        print(f"Kafka Error: {msg.error()}")
        continue

    try:
        topic = msg.topic()

        handler = TOPIC_HANDLERS.get(topic)

        if handler is None:
            print(f"No handler found for topic {topic}")
            continue

        event = json.loads(
            msg.value().decode("utf-8")
        )

        handler(
            event=event,
            offset=msg.offset()
        )

        # Commit only after successful ClickHouse write
        consumer.commit(message=msg)

    except Exception as exc:
        print(
            f"Failed processing "
            f"{topic}: {exc}"
        )