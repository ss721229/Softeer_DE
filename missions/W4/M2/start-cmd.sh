#!/bin/bash

service ssh start

if [ "$ROLE" = "master" ]; then
  $SPARK_HOME/sbin/start-master.sh
  
elif [ "$ROLE" = "worker" ]; then
  $SPARK_HOME/sbin/start-worker.sh spark://master:7077
else
  echo "[ERROR] Unknown role: $ROLE"
  exit 1
fi

echo "[INFO] Spark $ROLE is running. Container will stay alive."
tail -f /dev/null
