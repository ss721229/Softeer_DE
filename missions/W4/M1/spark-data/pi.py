import sys
from random import random
from operator import add
from pyspark.sql import SparkSession

if __name__ == "__main__":
    """
        Usage: pi [partitions]
    """
    spark = SparkSession \
        .builder \
        .appName("PythonPi") \
        .getOrCreate()

    partitions = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    output_path = "/opt/spark-data/pi_result"  # ✅ 저장 경로
    n = 100000 * partitions

    def f(_: int) -> float:
        x = random() * 2 - 1
        y = random() * 2 - 1
        return 1 if x ** 2 + y ** 2 <= 1 else 0

    count = spark.sparkContext.parallelize(range(1, n + 1), partitions).map(f).reduce(add)
    pi_value = 4.0 * count / n

    print(f"Pi is roughly {pi_value}")

    # ✅ DataFrame으로 변환 후 CSV 저장
    df = spark.createDataFrame([(pi_value,)], ["pi"])
    df.coalesce(1).write.mode("overwrite").option("header", "true").csv(output_path)

    spark.stop()