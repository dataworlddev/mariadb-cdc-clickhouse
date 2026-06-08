import time
from datetime import datetime, timezone 
from clickhouse_client import client

def to_decimal(v):
    try:
        return round(float(v), 2)
    except:
        return 0.0
    
def process_orders(event, offset):

    payload = event["payload"]
    op = payload["op"]

    if op in ("c", "u", "r"):
        row = payload["after"]
    elif op == "d":
        row = payload["before"]
    else:
        return

    event_ts = datetime.fromtimestamp(
        payload["ts_ms"] / 1000,
        tz=timezone.utc
    )

    print("RAW AMOUNT:", row["amount"], type(row["amount"]))
    client.insert(
        "raw.orders",
        [[
            row["id"],
            row["user_id"],
            to_decimal(row["amount"]),
            row["status"],
            op,
            event_ts,
            offset
        ]],
        column_names=[
            "id",
            "user_id",
            "amount",
            "status",
            "operation",
            "event_ts",
            "kafka_offset"
        ]
    )