import os

from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.functions import from_json, col, date_format
from pyspark.sql.types import StructType, StructField, DoubleType


def get_spark():
    context = SparkContext.getOrCreate()
    spark = SQLContext(context)
    return spark


def transform(df):
    for column in ["key", "value"]:
        df = df.withColumn(column, col(column).cast("string"))

    double_columns = ["humidity", "pressure", "temperature"]
    json_schema = StructType(
        [StructField(column, DoubleType(), True) for column in double_columns]
    )

    df = (
        df.withColumn("value", from_json(col("value"), json_schema))
        .withColumn("year", date_format(col("timestamp"), "yyyy"))
        .withColumn("month", date_format(col("timestamp"), "MM"))
        .withColumn("day", date_format(col("timestamp"), "dd"))
    )
    return df


def start_stream(broker_server, topic_name):
    spark = get_spark()

    df = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", broker_server)
        .option("subscribe", topic_name)
        .load()
    )

    df = transform(df)

    process = df.writeStream.trigger(processingTime="5 second").start(
        path="/raw",
        checkpointLocation="/checkpoint/raw",
        partitionBy=["year", "month", "day"],
    )
    return process


if __name__ == '__main__':
    broker_server = os.getenv("BROKER_SERVER")
    topic_name = os.getenv("TOPIC_NAME")

    process = start_stream(broker_server, topic_name)
    process.awaitTermination()
