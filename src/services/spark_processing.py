from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, window
from pyspark.sql.types import StructType, StructField, StringType, TimestampType
from core.config import settings
import logging

logger = logging.getLogger(__name__)

class SparkProcessingService:
    def __init__(self):
        self.spark = SparkSession.builder \
            .appName("SecurityEventProcessing") \
            .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2") \
            .getOrCreate()
        
        self.event_schema = StructType([
            StructField("event_type", StringType(), True),
            StructField("timestamp", TimestampType(), True),
            StructField("source_ip", StringType(), True),
            StructField("destination_ip", StringType(), True),
            StructField("severity", StringType(), True),
            StructField("description", StringType(), True),
            StructField("user_id", StringType(), True),
            StructField("device_id", StringType(), True)
        ])

    def process_events(self):
        df = self.spark \
            .readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", settings.KAFKA_SERVER) \
            .option("subscribe", settings.KAFKA_TOPIC) \
            .load()

        parsed_df = df.select(
            from_json(col("value").cast("string"), self.event_schema).alias("event")
        ).select("event.*")

        windowed_counts = parsed_df \
            .withWatermark("timestamp", "1 minute") \
            .groupBy(
                window("timestamp", "5 minutes"),
                "event_type",
                "severity"
            ) \
            .count()

        query = windowed_counts \
            .writeStream \
            .outputMode("complete") \
            .format("console") \
            .start()

        query.awaitTermination()

    def stop(self):
        self.spark.stop()

spark_service = SparkProcessingService()

def start_spark_processing():
    try:
        logger.info("Starting Spark processing service...")
        spark_service.process_events()
    except Exception as e:
        logger.error(f"Error in Spark processing: {e}")
    finally:
        spark_service.stop()

if __name__ == "__main__":
    start_spark_processing()
