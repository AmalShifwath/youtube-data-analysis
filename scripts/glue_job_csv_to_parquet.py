import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsgluedq.transforms import EvaluateDataQuality
from pyspark.sql.functions import input_file_name, regexp_extract
from awsglue.dynamicframe import DynamicFrame

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Default ruleset used by all target nodes with data quality enabled
DEFAULT_DATA_QUALITY_RULESET = """
    Rules = [
        ColumnCount > 0
    ]
"""

# Read CSVs from S3 using Spark for better encoding and error handling
df = spark.read \
    .format("csv") \
    .option("header", "true") \
    .option("multiLine", "false") \
    .option("quote", "\"") \
    .option("sep", ",") \
    .option("mode", "PERMISSIVE") \
    .load("s3://amal-de-youtube-analysis-raw-dev/raw_statistics_csv/")

# Add partition_0 from folder path
df = df.withColumn("partition_0", regexp_extract(input_file_name(), r"raw_statistics_csv/([^/]+)/", 1))

# Convert to DynamicFrame
AmazonS3rawcsv_node1748991274137 = DynamicFrame.fromDF(df, glueContext, "AmazonS3rawcsv_node1748991274137")

# Apply schema mapping
ChangeSchema_node1748991832474 = ApplyMapping.apply(
    frame=AmazonS3rawcsv_node1748991274137,
    mappings=[
        ("video_id", "string", "video_id", "string"),
        ("trending_date", "string", "trending_date", "string"),
        ("title", "string", "title", "string"),
        ("channel_title", "string", "channel_title", "string"),
        ("category_id", "string", "category_id", "bigint"),
        ("publish_time", "string", "publish_time", "string"),
        ("tags", "string", "tags", "string"),
        ("views", "string", "views", "bigint"),
        ("likes", "string", "likes", "bigint"),
        ("dislikes", "string", "dislikes", "bigint"),
        ("comment_count", "string", "comment_count", "bigint"),
        ("thumbnail_link", "string", "thumbnail_link", "string"),
        ("comments_disabled", "string", "comments_disabled", "string"),
        ("ratings_disabled", "string", "ratings_disabled", "string"),
        ("video_error_or_removed", "string", "video_error_or_removed", "string"),
        ("description", "string", "description", "string"),
        ("partition_0", "string", "partition_0", "string")
    ],
    transformation_ctx="ChangeSchema_node1748991832474"
)

# Data Quality Check
EvaluateDataQuality().process_rows(
    frame=ChangeSchema_node1748991832474,
    ruleset=DEFAULT_DATA_QUALITY_RULESET,
    publishing_options={
        "dataQualityEvaluationContext": "EvaluateDataQuality_node1748991117975",
        "enableDataQualityResultsPublishing": True
    },
    additional_options={
        "dataQualityResultsPublishing.strategy": "BEST_EFFORT",
        "observations.scope": "ALL"
    }
)

# Write to S3 partitioned by partition_0
AmazonS3cleanedcsv_node1748991912412 = glueContext.write_dynamic_frame.from_options(
    frame=ChangeSchema_node1748991832474,
    connection_type="s3",
    format="glueparquet",
    connection_options={
        "path": "s3://amal-de-youtube-analysis-cleaned-dev/raw_statistics_csv/",
        "partitionKeys": ["partition_0"]
    },
    format_options={"compression": "snappy"},
    transformation_ctx="AmazonS3cleanedcsv_node1748991912412"
)

job.commit()