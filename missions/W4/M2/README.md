## W4M1 수행 과정

### download data
- yellow taxi data 수집 (로컬)
``` shell
python spark-data/download_data.py
```
- 이후 날씨 데이터 수집을 위한 도시에 대한 위도, 경도 data 수집 (로컬)
``` shell
python spark-data/get_pos.py
```

### Dockerfile
- w4m2 이미지 빌드 전 w4m1 이미지 필요
- `https://github.com/ss721229/Softeer_DE/tree/main/missions/W4/M1`의 Dockerfile로 w4m1 이미지 빌드 가능
``` shell
docker build -t w4m1 .
docker build -t w4m2 .
```

### docker-compose
- docker-compose 수행 (Master 1, Worker 2)
- Master Web UI : http://localhost:8080
``` shell
docker-compose -f docker-compose.yaml up -d
```

### jupyter notebook
``` shell
docker exec -it master jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token='' --NotebookApp.password=''
```
