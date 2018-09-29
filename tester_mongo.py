import net_tester
import pymongo

class MongoTester(net_tester.Tester):
    def __init__(self, db_addr, db_name, gateway_ip, ping_ip, servers=[]):
        net_tester.Tester.__init__(self, gateway_ip, ping_ip, servers)
        self.mongoclient = pymongo.MongoClient(db_addr)
        self.db = self.mongoclient[db_name]

    def write_gatewaycheck(self, is_online, time):
        col = self.db["gatewaychecks"]
        newdict = {
            "time": time,
            "is_online": is_online
            }
        col.insert_one(newdict)

    def write_pingcheck(self, is_success, mean_ping, time):
        col = self.db["pingchecks"]
        newdict = {
            "time": time,
            "is_success": is_success,
            "mean_ping": mean_ping
            }
        col.insert_one(newdict)

    def write_speedtest(self, download, upload, ping, serverurl, servername, time):
        col = self.db["speedtests"]
        newdict = {
            "time": time,
            "upload": upload,
            "download": download,
            "ping": ping,
            "serverurl": serverurl,
            "servername": servername
            }
        col.insert_one(newdict)
