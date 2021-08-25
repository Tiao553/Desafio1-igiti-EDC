from pyspark.sql import SparkSession

DATALAKE_PATH_LADING = "s3://landing-zone-531477333755/"
DATALAKE_PATH_PROCESSING = "s3://processing-zone-531477333755/"

if __name__ == '__main__':

    spark = (
        SparkSession
        .builder
        .appName('Censo Job')
        .getOrCreate()
    )

    # Load csv file from datalake
    censo = (
        spark
        .read
        .format("csv")
        .option("inferSchema", True)
        .option("delimiter", "|")
        .option("header", True)
        .load(DATALAKE_PATH_LADING+ "censo/data/matricula*.csv")
    )

    try:
        # Save the file in the processing zone with parquet format
        (
            censo
            .write
            .mode("overwrite")
            .format("parquet")
            .partitionBy("CO_UF")
            .save(DATALAKE_PATH_PROCESSING + "censo/")
        )

    except Exception as err:
        print(err)

