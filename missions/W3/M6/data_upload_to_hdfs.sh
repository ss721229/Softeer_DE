#!/bin/bash

UPLOAD_DATA=/Users/admin/Desktop/Softeer_DE/data/aws_reviews/ext
CONTAINER_NAME=namenode
HDFS_TARGET_DIR=/user/root/aws_reviews

docker exec -it $CONTAINER_NAME hadoop fs -mkdir -p $HDFS_TARGET_DIR

for file in "$UPLOAD_DATA"/*.jsonl; do
    filename=$(basename "$file")
    echo "📦 Uploading $filename to HDFS..."

    # 컨테이너에 복사
    docker cp "$file" $CONTAINER_NAME:/tmp/$filename

    # HDFS에 업로드
    docker exec -it $CONTAINER_NAME hadoop fs -put -f /tmp/$filename $HDFS_TARGET_DIR/

    # 컨테이너 내 임시 파일 삭제
    docker exec -it $CONTAINER_NAME rm -f /tmp/$filename

    echo "✅ Uploaded: $filename"
done

echo "🎉 All files uploaded to HDFS: $HDFS_TARGET_DIR"