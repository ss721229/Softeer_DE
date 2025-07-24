## W3M2 수행 과정

### Docker Image Build
- `Dockerfile`이 존재하는 디렉터리에서 실행
``` shell
docker build -t w3m2b .
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

### Hadoop 구성 변경 및 검증 자동화
- 로컬에서 Hadoop 구성 변경 및 검증 자동화 수행
``` shell
bash auto-config-modification.sh
```
