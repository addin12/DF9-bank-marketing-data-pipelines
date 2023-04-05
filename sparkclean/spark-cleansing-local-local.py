import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.functions import when
from pyspark.sql.functions import regexp_replace
from pyspark.sql.functions import to_date, date_format
from pyspark.sql.functions import concat, lit

# Creating the spark session
spark = SparkSession.builder \
    .master("local[*]") \
    .appName("finalprojclean") \
    .config("spark.sql.inferSchema", "true")\
    .getOrCreate()

# Read the csv file
df = spark.read.format("parquet").option("header", "true").load("bank-additional-full-masked-null.parquet")

# 1. Standardize the education value
df = df.withColumn("education",
                                        when(df.education.endswith('4y'), regexp_replace(df.education, 'basic.4y', 'basic')) \
                                        .when(df.education.endswith('6y'), regexp_replace(df.education, 'basic.6y', 'basic')) \
                                         .when(df.education.endswith('9y'), regexp_replace(df.education, 'basic.9y', 'basic')) \
                                         .otherwise(df.education)
                                        )

# 2. Some column name need to be standardized because Spark & BigQuery can't read it
df = df.withColumnRenamed('emp.var.rate', 'emp_var_rate') \
       .withColumnRenamed('cons.price.idx', 'cons_price_idx') \
       .withColumnRenamed('cons.conf.idx', 'cons_conf_idx') \
       .withColumnRenamed('nr.employed', 'nr_employed') \
       .withColumnRenamed('default', 'credit')

# 3. Dropping null value
df = df.na.drop("any")

# 4. Change the month data type into date
df = df.withColumn("date", to_date("month", "MMM").alias("date")) \
       .withColumn("date", date_format("date", "MM").alias("date"))

# 5. Combine the month and year value in date column
df = df.withColumn("date2", concat(df["year"], lit("-"), df["date"])) \
       .withColumn("date2", date_format("date2", "yyyyMM")) \
       .withColumn("date2", to_date("date2", "yyyyMM")) \
       .drop("date", "month", "year")
    
df = df.withColumnRenamed('date2', 'date')

# Save as CSV file
df.toPandas().to_csv("bank-marketing.csv", index=False)  


