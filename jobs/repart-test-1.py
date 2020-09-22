import __main__
from os import environ, listdir, path
import json
from pyspark import SparkFiles
from pyspark.sql import SparkSession

# from dependencies import logging

from pyspark.sql import Row
from pyspark.sql.functions import col, concat_ws, lit



def start_spark(app_name='my_spark_app', master='local[*]', jar_packages=[], files=[], spark_config={}):
    # detect execution environment
    flag_repl = not(hasattr(__main__, '__file__'))
    flag_debug = 'DEBUG' in environ.keys()

    if not (flag_repl or flag_debug):
        # get Spark session factory
        spark_builder = (
            SparkSession
            .builder
            .appName(app_name))
    else:
        # get Spark session factory
        spark_builder = (
            SparkSession
            .builder
            .master(master)
            .appName(app_name))

        # create Spark JAR packages string
        spark_jars_packages = ','.join(list(jar_packages))
        spark_builder.config('spark.jars.packages', spark_jars_packages)

        spark_files = ','.join(list(files))
        spark_builder.config('spark.files', spark_files)

        # add other config params
        for key, val in spark_config.items():
            spark_builder.config(key, val)

    # create session and retrieve Spark logger object
    spark_sess = spark_builder.getOrCreate()
    spark_logger = Log4j(spark_sess)

    return spark_sess, spark_logger
    
def main():
    spark, log = start_spark(
            app_name='repart-test-1')

    # create spark context
    sc = spark.sparkContext

    # log that main ETL job is starting
    log.warn('repart-test-1 is up-and-running')

    baseRDD = sc.parallelize([1, 4, 6, 7, 2, 3, 8, 42])

    log.warn (baseRDD.collect())

    # log the success and terminate Spark application
    log.warn('test_repart-test-1 is finished')
    spark.stop()
    return None






class Log4j(object):
    """Wrapper class for Log4j JVM object.

    :param spark: SparkSession object.
    """

    def __init__(self, spark):
        # get spark app details with which to prefix all messages
        conf = spark.sparkContext.getConf()
        app_id = conf.get('spark.app.id')
        app_name = conf.get('spark.app.name')

        log4j = spark._jvm.org.apache.log4j
        message_prefix = '<' + app_name + ' ' + app_id + '>'
        self.logger = log4j.LogManager.getLogger(message_prefix)

    def error(self, message):
        """Log an error.

        :param: Error message to write to log
        :return: None
        """
        self.logger.error(message)
        return None

    def warn(self, message):
        """Log an warning.

        :param: Error message to write to log
        :return: None
        """
        self.logger.warn(message)
        return None

    def info(self, message):
        """Log information.

        :param: Information message to write to log
        :return: None
        """
        self.logger.info(message)
        return None


if __name__ == '__main__':
    main()