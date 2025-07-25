## W3M4 수행 과정

### HDFS 작업 수행
- sentiment140 file upload 수행
``` shell
# 로컬에서 컨테이너로 파일 복사
docker cp "./sentiment140.csv" namenode:/tmp/sentiment140.csv

# 컨테이너에서 HDFS로 업로드
docker exec -it namenode hadoop fs -put /tmp/sentiment140.csv /user/root/
```
- Mapper, Reducer 파일 업로드
``` shell
docker cp mapper.py namenode:/tmp/mapper.py
docker cp reducer.py namenode:/tmp/reducer.py
docker exec -it namenode chmod +x /tmp/mapper.py
docker exec -it namenode chmod +x /tmp/reducer.py
```

### MapReduce 실행 및 결과 확인
- MapReduce 실행
``` shell
docker exec -it namenode mapred streaming \
  -files /tmp/mapper.py,/tmp/reducer.py \
  -input /user/root/sentiment140.csv \
  -output  /user/root/output \
  -mapper mapper.py \
  -reducer reducer.py
```
- MapReduce 결과 확인
``` shell
docker exec -it namenode hadoop fs -cat output/part-00000
```