from time import sleep
import psycopg2
import pymongo
client = pymongo.MongoClient("mongodb+srv://saud:mlab3431@hospitals.5loco.mongodb.net/helpagainstcovid?retryWrites=true&w=majority")

mydatabase = client.helpagainstcovid

def get_data():
    latlong=[]

    db = client.dbsaud
    data = dict()
    id = 0
    collection = mydatabase.hospitalsinfo
    cursor = collection.find()
    for record in cursor:
        print(record['name'])
        sp=record['latlong'].split(',')
        lat,long = sp[0],sp[1]
        print(lat,long)
        data[id] = {"hospital": record['name'], "state": 'Maharashtra', "district": 'Mumbai',
                                "address": record['hpinfo'], "latitude": lat,
                                "longitude": long, "country": 'India', "beds":record['bedinfo']}
        id = id + 1
        #if id == 8:   #temp
        #     break
    return data
 
def plasma_data():
    latlong=[]
    db = client.dbsaud
    data = dict()
    id = 0
    collection = mydatabase.plasmadata
    cursor = collection.find()
    for record in cursor:
        print(record['info'])
        lat=record['latlong'][1]
        print(lat)
        long = record['latlong'][0]
        print(long)
        print(lat,long)
        data[id] = {"binfo": record['info'], "state": 'Maharashtra', "district": 'Mumbai',
                                "address": record['type'], "latitude": lat,
                                "longitude": long, "country": 'India', "beds":record['avail']}
        id = id + 1
        #if id == 8:   #temp
        #     break
    return data

