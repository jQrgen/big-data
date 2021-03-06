"""
Import and edit the result from task1.py.
task1.py's output can be found in foursquare-data/foursquare_edit/part-xxxxx
- johan
"""

from datetime import datetime
from datetime import timedelta
from math import *
from pyspark import SparkConf
from pyspark import SparkContext
import sys

# Script functions to edit data
def remove_excess(data):
	line = data.split("\t")
	line.pop() # pop the city type
	line.pop() # pop the country fullname
	result = "\t".join(line)
	return result

def assign_location(foursquare_data):
    foursquare_line = foursquare_data.split("\t")
    lat = float(foursquare_line[5])
    lon = float(foursquare_line[6])
    distance = sys.maxint
    city = None
    country = None
    for city_data in cities_collection:
        city_line = city_data.split("\t")
        temp_distance = haversine(lat, lon, 
                                    float(city_line[1]), float(city_line[2]))
        if (temp_distance < distance):
            distance = temp_distance
            city = city_line[0]
            country = city_line[3]
    foursquare_line.append(city)
    foursquare_line.append(country)
    result = "\t".join(foursquare_line)
    return result
    
def haversine(lat1, lon1, lat2, lon2):

	# convert decimal degrees to radians
	lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

	# haversine formula
	dlon = lon2 - lon1
	dlat = lat2 - lat1
	a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
	c = 2 * asin(sqrt(a))
	r = 6371 # Radius of earth in kilometers. Use 3956 for miles
	return c * r

# Create a spark context
conf = (SparkConf()
         .setMaster("local[4]")
         .setAppName("My app")
         .set("spark.executor.memory", "6g"))
sc = SparkContext(conf = conf)

# Print some SparkConf variables
print "\nSparkConf variables: ", conf.toDebugString()
print "\nSparkConf id: ", sc.applicationId
print "\nUser: ", sc.sparkUser()
print "\nVersion: ", sc.version

# Import data
cities_data = sc.textFile("foursquare-data/dataset_TIST2015_Cities.txt",
                            use_unicode=False)
foursquare_data = sc.textFile("foursquare-data/foursquare_edit/part-*",
                                use_unicode=False)

# Provoke action in dataset
cities_data = cities_data.map(remove_excess)
#c_data_type = type(cities_data) 
#c_count = cities_data.count()
#c_first = cities_data.first()
#c_top_5 = cities_data.top(5)
cities_collection = cities_data.collect()
#cities_collection_type = type(cities_collection)
foursquare_data = foursquare_data.map(assign_location)
#fq_data_type = type(foursquare_data)
#fq_count = foursquare_data.count()
#fq_first = foursquare_data.first()
#fq_top_5 = foursquare_data.top(5)

# Print some data information
#print "\n### CITIES_DATA ###"
#print "\ncities_data filetype: ", c_data_type
#print "\nNumber of elements: ", c_count
#print "\nFirst element in the dataset: ", c_first
#print "\nTop 5 elements in the dataset: ", c_top_5
#print "\ncities_collection type: ", cities_collection_type
#print "\n### FOURSQUARE_DATA ###"
#print "\nfoursquare_data filetype: ", fq_data_type
#print "\nNumber of elements: ", fq_count
#print "\nFirst element in the dataset: ", fq_first
#print "\nTop 5 elements in the dataset: ", fq_top_5

# Save the data (Choose a directory of your own choosing)
foursquare_data.saveAsTextFile("foursquare-data/foursquare_edit2")

# Stop the spark context
sc.stop()
