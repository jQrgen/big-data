"""
Import and edit the result from task1.py.
task1.py's output can be found in foursquare-data/foursquare_edit/part-xxxxx
- johan
"""

from datetime import datetime
from datetime import timedelta
from pyspark import SparkConf
from pyspark import SparkContext

conf = (SparkConf()
         .setMaster("local")
         .setAppName("My app")
         .set("spark.executor.memory", "1g"))
sc = SparkContext(conf = conf)

foursquare_data = sc.textFile("foursquare-data/foursquare_edit/part-00000")

foursquare_data.saveAsHadoopDataset("foursquare/hadoop_dataset")
