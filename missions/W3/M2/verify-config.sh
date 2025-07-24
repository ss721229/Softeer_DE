#!/bin/bash

HADOOP_HOME=/opt/hadoop
HDFS_DIR=/tmp/hdfs_test_dir
TEST_FILE_LOCAL=/tmp/testfile.txt
TEST_FILE_HDFS=$HDFS_DIR/testfile.txt
EXPECTED_REPLICATION=2
EXPECTED_BLOCKSIZE=134217728
EXPECTED_TMP_DIR="/hadoop/tmp"
EXPECTED_BUFFER_SIZE=131072
EXPECTED_SORT_MB=256
EXPECTED_RM_HOST=namenode
EXPECTED_NM_MEM_MB=8192
EXPECTED_MIN_ALLOC_MB=1024

echo "====== [1] 기본 파일시스템 확인 ======"
fs_default=$($HADOOP_HOME/bin/hdfs getconf -confKey fs.defaultFS)
echo "fs.defaultFS: $fs_default"
[[ "$fs_default" == "hdfs://$EXPECTED_RM_HOST:9000" ]] && echo "✅ 기본 파일시스템 OK" || echo "❌ 기본 파일시스템 불일치"

echo -e "\n====== [2] 설정값 확인 ======"
conf_check() {
  key=$1
  expected=$2
  value=$($HADOOP_HOME/bin/hdfs getconf -confKey "$key" 2>/dev/null)
  [[ "$value" == "$expected" ]] && echo "✅ $key = $value" || echo "❌ $key = $value (예상: $expected)"
}
conf_check io.file.buffer.size $EXPECTED_BUFFER_SIZE
conf_check hadoop.tmp.dir $EXPECTED_TMP_DIR
conf_check dfs.blocksize $EXPECTED_BLOCKSIZE
conf_check dfs.namenode.name.dir "/hadoop/dfs/name"
conf_check mapreduce.task.io.sort.mb $EXPECTED_SORT_MB
conf_check yarn.resourcemanager.hostname $EXPECTED_RM_HOST
conf_check yarn.nodemanager.resource.memory-mb $EXPECTED_NM_MEM_MB
conf_check yarn.scheduler.minimum-allocation-mb $EXPECTED_MIN_ALLOC_MB

echo -e "\n====== [3] 테스트 파일 작성 및 업로드 ======"
echo "This is a test file" > $TEST_FILE_LOCAL
$HADOOP_HOME/bin/hdfs dfs -mkdir -p $HDFS_DIR
$HADOOP_HOME/bin/hdfs dfs -put -f $TEST_FILE_LOCAL $TEST_FILE_HDFS

echo -e "\n====== [4] 복제 수 확인 ======"
rep_factor=$(hdfs getconf -confKey dfs.replication)

if [[ "$rep_factor" == "$EXPECTED_REPLICATION" ]]; then
  echo "✅ 복제 수 = $rep_factor"
else
  echo "❌ 복제 수 = $rep_factor (예상: $EXPECTED_REPLICATION)"
fi

echo -e "\n====== [5] WordCount MapReduce 실행 ======"
$HADOOP_HOME/bin/hdfs dfs -rm -r -skipTrash $HDFS_DIR/output &>/dev/null
$HADOOP_HOME/bin/hadoop jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-*.jar wordcount $HDFS_DIR $HDFS_DIR/output
if $HADOOP_HOME/bin/hdfs dfs -ls $HDFS_DIR/output/part-r-00000 &>/dev/null; then
  echo "✅ MapReduce 작업 성공"
else
  echo "❌ MapReduce 작업 실패"
fi

echo -e "\n====== [6] YARN ResourceManager 메모리 조회 ======"
RM_HTTP_ADDR="$EXPECTED_RM_HOST:8088"
MEM_JSON=$(curl -s http://$RM_HTTP_ADDR/ws/v1/cluster/metrics)
if [[ -n "$MEM_JSON" ]]; then
  total_mem=$(echo $MEM_JSON | grep -oP '"totalMB"\s*:\s*\K[0-9]+')
  echo "YARN 총 메모리: $total_mem MB"
  [[ "$total_mem" -ge "$EXPECTED_NM_MEM_MB" ]] && echo "✅ 메모리 OK" || echo "❌ 메모리 부족 (총 $total_mem MB)"
else
  echo "❌ ResourceManager REST API 응답 실패 (http://$RM_HTTP_ADDR)"
fi

echo -e "\n====== 완료 ======"
