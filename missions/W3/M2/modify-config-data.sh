#!/bin/bash

# 1. 변경 파일 덮어쓰기
cp /modify-config/*.xml $HADOOP_HOME/etc/hadoop/
echo "새로운 설정 파일 적용 완료"

# 2. 현재 적용된 설정 확인
echo "현재 설정 요약:"
grep -h "<name>\|<value>" $HADOOP_HOME/etc/hadoop/*.xml | sed 'N;s/\n/ = /' | sort | uniq | head -n 20

# 3. Hadoop 재시작
echo "Hadoop 서비스 재시작 중..."

# Stop all services
$HADOOP_HOME/bin/hdfs --daemon stop datanode

# Start all services
$HADOOP_HOME/bin/hdfs namenode -format -force
$HADOOP_HOME/bin/hdfs --daemon start datanode

echo "Hadoop 서비스 재시작 완료"
