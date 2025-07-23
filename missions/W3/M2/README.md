## W3M2 수행 과정

### Docker Image Build
- `Dockerfile`이 존재하는 디렉터리에서 실행
``` shell
docker build -t w3m2 .
```

### Docker Compose Up
- `docker-compose.yaml`이 존재하는 디렉터리에서 실행
- 1개의 namenode, 3개의 datanode 존재 (하나의 datanode는 마스터 노드에 존재)
``` shell
docker-compose -f docker-compose.yaml up
```

### Hadoop Web UI Monitoring
- YARN Port : 8088
- NameNode Port : 9870
- DataNode Port : 9864, 9865
- `localhost:8088`에서 클러스터 모니터링
- `localhost:9870`에서 네임 노드, HDFS에 존재하는 파일 모니터링
- `localhost:9864`에서 데이터 노드 모니터링

### HDFS 작업 수행
- 로컬에서 file upload 수행
``` shell
# 로컬에서 컨테이너로 파일 복사
docker cp ./data.csv <Namenode Container ID>:/tmp/data.csv

# 컨테이너에서 HDFS로 업로드
docker exec -it <Namenode Container ID> hadoop fs -put /tmp/data.csv /user/root/
```

### MapReduce 작업 수행
- Docker 내부에서 wordcount 수행
``` shell
# MapReduce를 위한 디렉터리 생성
hadoop fs -mkdir wordcount
hadoop fs -mkdir wordcount/input

# wordcount를 수행하기 위한 test 파일 생성 및 HDFS에 업로드
echo "hello hadoop hadoop test" > /tmp/test.txt
hdfs dfs -put /tmp/test.txt wordcount/input/test.txt

# MapReduce 수행
hadoop jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-*.jar wordcount wordcount/input wordcount/output

# 결과 확인
hdfs dfs -cat wordcount/output/part-r-00000
```
