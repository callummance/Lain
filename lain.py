#!/dev/python3

import net_monitor
import tester_mongo

import json
import datetime

def start_monitoring(conf_file):
    conf = json.load(conf_file)
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
    with open("./lain.json") as conf:
        start_monitoring(conf)