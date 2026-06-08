curl -X POST http://localhost:8083/connectors \
-H "Content-Type: application/json" \
-d @debezium/connector.json
# status check after submiting job
# curl http://localhost:8083/connectors/mariadb-cdc/status
# expected output :
#  {
#   "connector": {
#     "state": "RUNNING"
#   },
#   "tasks": [
#     {
#       "state": "RUNNING"
#     }
#   ]
# } 