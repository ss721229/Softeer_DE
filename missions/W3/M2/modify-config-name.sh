#!/bin/bash

# 1. 원본 파일 백업
mkdir -p /hadoop/config-backup
time=$(date +%Y-%m-%d_%H:%M:%S)
mkdir -p /hadoop/config-backup/$time

cp $HADOOP_HOME/etc/hadoop/core-site.xml /hadoop/config-backup/$time
cp $HADOOP_HOME/etc/hadoop/hdfs-site.xml /hadoop/config-backup/$time
cp $HADOOP_HOME/etc/hadoop/mapred-site.xml /hadoop/config-backup/$time
cp $HADOOP_HOME/etc/hadoop/yarn-site.xml /hadoop/config-backup/$time

echo "기존 설정 파일 백업 완료: /hadoop/config-backup/$time"

# 2. 변경 파일 덮어쓰기
cp /modify-config/*.xml $HADOOP_HOME/etc/hadoop/
echo "새로운 설정 파일 적용 완료"

# 3. 현재 적용된 설정 확인
echo "현재 설정 요약:"
grep -h "<name>\|<value>" $HADOOP_HOME/etc/hadoop/*.xml | sed 'N;s/\n/ = /' | sort | uniq | head -n 20

# 4. Hadoop 재시작
echo "Hadoop 서비스 재시작 중..."

# Stop all services
$HADOOP_HOME/sbin/stop-dfs.sh
$HADOOP_HOME/sbin/stop-yarn.sh

# Start all services
$HADOOP_HOME/bin/hdfs namenode -format -force
$HADOOP_HOME/sbin/start-dfs.sh
$HADOOP_HOME/sbin/start-yarn.sh

echo "Hadoop 서비스 재시작 완료"
