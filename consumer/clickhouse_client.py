from clickhouse_connect import get_client
from dotenv import load_dotenv
import os

load_dotenv()

client = get_client(
    host=os.getenv("CLICKHOUSE_HOST", "clickhouse"),
    port=int(os.getenv("CLICKHOUSE_PORT", "8123")),
    username=os.getenv("CLICKHOUSE_USER" , "default"),
    password=os.getenv("CLICKHOUSE_PASSWORD", ""),
)