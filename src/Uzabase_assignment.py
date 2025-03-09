# -- coding: utf-8 --
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lower, udf, lit, explode, split
from pyspark.sql.types import IntegerType
import re
import sys
import os
from datasets import load_dataset

# Function to count occurrences of words in a description
def count_word_in_text(word, text):
    return len(re.findall(r'\b' + re.escape(word) + r'\b', text))

# Register UDF
count_word_udf = udf(count_word_in_text, IntegerType())

def process_data(cfg, dataset, dirout):
    # Initialize Spark session
    spark = SparkSession.builder \
        .appName("example") \
        .config("spark.submit.pyFiles", "/app/src/Uzabase_assignment.py") \
        .getOrCreate()

    # Load the dataset with debugging
    try:
        data = load_dataset("ag_news", split="test")  # Use the correct dataset identifier
        print("Dataset loaded successfully:", data)
    except Exception as e:
        print("Error loading dataset:", e)
        raise

    # Convert the dataset to a PySpark DataFrame
    df = spark.createDataFrame(data)

    # Words to count
    words_to_count = ["president", "the", "Asia"]

    # Prepare the table with word and count
    word_counts = []

    # Loop over the words and count occurrences in the 'text' column
    for word in words_to_count:
        word_count_df = df.withColumn("word_count", count_word_udf(lit(word), col("text")))  # Use 'text' instead of 'description'
        word_count = word_count_df.select("word_count").agg({"word_count": "sum"}).collect()[0][0]
        word_counts.append((word, word_count))

    # Create DataFrame with word counts
    result_df = spark.createDataFrame(word_counts, ["word", "word_count"])

    # Save the table as a Parquet file
    result_df.write.parquet(f"{dirout}/word_count_{spark.sql('select current_date()').collect()[0][0]}.parquet")

def process_data_all(cfg, dataset, dirout):
    spark = SparkSession.builder.appName("example").getOrCreate()
    data = load_dataset("sh0416/ag_news", split="test")
    df = spark.createDataFrame(data)

    # Tokenize the 'description' column to split words and remove unwanted characters
    words_df = df.withColumn("words", explode(split(lower(col("description")), r'\W+')))

    # Remove empty words
    words_df = words_df.filter(words_df["words"] != "")

    # Count the frequency of each unique word
    word_counts_all = words_df.groupBy("words").count().withColumnRenamed("count", "word_count")

    # Save the table as a Parquet file
    word_counts_all.write.mode('overwrite').parquet(f"{dirout}/word_count_all_{spark.sql('select current_date()').collect()[0][0]}.parquet")
