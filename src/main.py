import os
from dynaconf import settings
from pyspark.sql import SparkSession
from pyspark.sql.functions import (col, lit)
from pyspark.sql.types import IntegerType

from src.ETLInterface import ETLInterface

class TestJob(ETLInterface):
	def __init__(self, spark: SparkSession):
		self.spark = spark
	
	def read_data(self):
		columns = ["value"]
		self.data = self.spark.createDataFrame([(1),(2),(3)], IntegerType()).toDF(*columns)

	def transform_data(self):
		self.data = self.data.withColumn("value_updated", col("value") + lit(1))

	def write_data(self):
		self.data.write.option("header", True).option(
                "truncate", "true"
            ).mode("overwrite").save(
                f"{settings.DATALAKE_PATH}/PreProcessedData", format="parquet"
        )

if __name__ == "__main__":

	## Regular Spark job executed on a Docker container
	os.environ["PYSPARK_PYTHON"] = "./pyspark_venv.pex"
	spark = (
		SparkSession.builder.appName("hellofresh_test")
		.master(f"spark://{settings.SPARK_HOST_URL}")
		.config("spark.files", "pyspark_venv.pex")
		.getOrCreate()
	)

	## Job Flow
	jobflow = TestJob(spark)
	jobflow.read_data()
	jobflow.transform_data()
	jobflow.write_data()
	## Stop Spark Session
	spark.stop()
