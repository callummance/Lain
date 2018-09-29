#!/usr/bin/env python3

import net_monitor
import tester_mongo
from statspage import server

import json
import datetime
import threading

def start_monitoring(conf):
    mongoconf = conf["mongo"]
    targetconf = conf["tests"]["targets"]
    timeconf = conf["tests"]["time_deltas"]
    t = tester_mongo.MongoTester(
        mongoconf["address"], 
        mongoconf["db"], 
        targetconf["gateway_ip"], 
        targetconf["ping_target"], 
        targetconf["speedtest_servers"]
        )
    m = net_monitor.NetMonitor(
        t, 
        datetime.timedelta(seconds=timeconf["gateway_check"]), 
        datetime.timedelta(seconds=timeconf["ping_check"]), 
        datetime.timedelta(seconds=timeconf["speed_test"])
    )
    m.start_monitoring()

if __name__ == "__main__":
    with open("./lain.json") as conf_file:
        conf = json.load(conf_file)
        t = threading.Thread(target=start_monitoring, args=[conf])
        t.daemon = True
        t.start()
        server.start_server(conf)
