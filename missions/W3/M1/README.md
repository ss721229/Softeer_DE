## W3M1 수행 과정

### Docker Image Build
- `Dockerfile` `core-site.xml` `hdfs-site.xml` `mapred-site.xml`이 존재하는 디렉터리에서 실행
``` shell
docker build -t w3m1 .
```

### Docker Container
- NameNode UI : 9870
- DataNode UI : 9864
- `localhost:9870`에서 네임 노드, HDFS에 존재하는 파일 모니터링
- `localhost:9864`에서 데이터 노드 모니터링
``` shell
docker run -it -p 9870:9870 -p 9864:9864 --name cont w3m1
```

### HDFS 작업 수행
- file upload 수행
``` shell
# 로컬에서 컨테이너로 파일 복사
docker cp ./data.csv <Container ID>:/tmp/data.csv

# 컨테이너에서 HDFS로 업로드
docker exec -it <Container ID> hadoop fs -put /tmp/data.csv /user/root/upload/
```
