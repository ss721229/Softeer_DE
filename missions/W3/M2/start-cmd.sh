#!/bin/bash

if [ "$ROLE" = "namenode" ] && [ ! -d "$HADOOP_HOME/data/namenode/current" ]; then
  echo "[INFO] Formatting HDFS NameNode..."
  $HADOOP_HOME/bin/hdfs namenode -format -force
fi

service ssh start

if [ "$ROLE" = "namenode" ]; then
  echo "[INFO] Starting NameNode and ResourceManager..."
  $HADOOP_HOME/sbin/start-dfs.sh
  $HADOOP_HOME/sbin/start-yarn.sh
elif [ "$ROLE" = "datanode" ]; then
  echo "[INFO] Starting DataNode and NodeManager..."
  $HADOOP_HOME/bin/hdfs --daemon start datanode
  $HADOOP_HOME/bin/yarn --daemon start nodemanager
else
  echo "[ERROR] Unknown role: $ROLE"
  exit 1
fi

# 필요한 디렉토리 생성 (마스터 노드에서만)
if [ "$ROLE" = "namenode" ]; then
  $HADOOP_HOME/bin/hdfs dfs -mkdir -p /user/root
fi

echo "[INFO] Hadoop $ROLE is running. Container will stay alive."
tail -f /dev/null
