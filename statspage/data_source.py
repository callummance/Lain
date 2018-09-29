import pymongo

def get_db_connection(conf):
    db_addr = conf["address"]
    db_name = conf["db"]
    mongoclient = pymongo.MongoClient(db_addr)
    return mongoclient[db_name]

def speedtest_data(conf, start_date=None, end_date=None):
    client_db = get_db_connection(conf)
    speedtests = client_db["speedtests"]
    query_dict = {"time": {"$exists": True}}
    if start_date != None:
        query_dict["time"]["$gt"] = start_date
    if end_date != None:
        query_dict["time"]["$lt"] = end_date
    return dict(enumerate(speedtests.find(query_dict, {"_id": False}).sort("time")))

def pingtest_data(conf, start_date=None, end_date=None):
    client_db = get_db_connection(conf)
    pingchecks = client_db["pingchecks"]
    query_dict = {"time": {"$exists": True}}
    if start_date != None:
        query_dict["time"]["$gt"] = start_date
    if end_date != None:
        query_dict["time"]["$lt"] = end_date
    return dict(enumerate(pingchecks.find(query_dict, {"_id": False}).sort("time")))

def gatewaytest_data(conf, start_date=None, end_date=None):
    client_db = get_db_connection(conf)
    gatewaytests = client_db["gatewaychecks"]
    query_dict = {"time": {"$exists": True}}
    if start_date != None:
        query_dict["time"]["$gt"] = start_date
    if end_date != None:
        query_dict["time"]["$lt"] = end_date
    return dict(enumerate(gatewaytests.find(query_dict, {"_id": False}).sort("time")))
