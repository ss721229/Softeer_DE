## W4M1 수행 과정

### Dockerfile
``` shell
docker build -t w4m1 .
```

### docker-compose
- docker-compose 수행 (Master 1, Worker 2)
- Master Web UI : http://localhost:8080
``` shell
docker-compose -f docker-compose.yaml up -d
```

### pi.py
- 결과를 저장하기 위해 예시 코드를 일부 변경
- `pi.py`와 output은 마운트한 디렉터리 (spark-data)에 저장
``` shell
spark-submit --master spark://master:7077 /opt/spark-data/pi.py

# 결과 확인
cat /opt/spark-data/pi_result/part-00000-*.csv
```
