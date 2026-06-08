from datetime import datetime, timezone
from clickhouse_client import client

def process_users(event, offset):

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

    client.insert(
        "raw.users",
        [[
            row["id"],
            row["name"],
            row["email"],
            op,
            event_ts,
            offset
        ]],
        column_names=[
            "id",
            "name",
            "email",
            "operation",
            "event_ts",
            "kafka_offset"
        ]
    )