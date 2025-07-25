## W3M6 수행 과정

### Amazon Product Reviews 다운로드
``` shell
python data_download.py
```

### HDFS 작업 수행
- file upload 수행
``` shell
bash data_upload_to_hdfs.sh
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
  -D mapreduce.reduce.memory.mb=4096 \
  -D mapreduce.reduce.java.opts=-Xmx3072m \
  -D mapreduce.map.memory.mb=2048 \
  -D mapreduce.map.java.opts=-Xmx1536m \
  -files /tmp/mapper.py,/tmp/reducer.py \
  -input /user/root/aws_reviews/ \
  -output  /user/root/output \
  -mapper mapper.py \
  -reducer reducer.py
```
- MapReduce 결과 확인 (20개)
``` shell
docker exec -it namenode hadoop fs -cat "output/part-*" | head -20
```