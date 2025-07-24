#!/bin/bash

# 컨테이너 이름 정의
NAMENODE=namenode
DATANODES=("datanode-1" "datanode-2")

# 실행할 스크립트 경로 (컨테이너 내부 경로)
MN_SCRIPT_PATH="/usr/local/bin/modify-config-name.sh"
DN_SCRIPT_PATH="/usr/local/bin/modify-config-data.sh"

# NameNode에 대해 설정 적용
echo "[INFO] NameNode에 설정 적용 중..."
docker exec $NAMENODE bash -c "$MN_SCRIPT_PATH"

# 각 DataNode에 대해 설정 적용
for DN in "${DATANODES[@]}"; do
  echo "[INFO] $DN에 설정 적용 중..."
  docker exec $DN bash -c "$DN_SCRIPT_PATH"
done

docker exec $NAMENODE bash verify-config.sh
