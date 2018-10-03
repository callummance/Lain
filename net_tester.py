import speedtest
import ipaddress
import datetime
from sys_ping import sys_ping

class Tester:
    def __init__(self, gateway_ip, ping_ip, servers=[]):
        self.s = speedtest.Speedtest()
        self.s.get_servers(servers)
        self.gateway_ip = gateway_ip
        self.ping_ip = ping_ip

    def run_pingcheck(self):
        now = datetime.datetime.utcnow()
        if res["success"]:
            res = sys_ping.run_pingcheck(self.ping_ip)
            self.write_pingcheck(res["success"], res["mean_ping"], now)
        else:
            self.write_failedpingcheck(now)

    def run_gatewaycheck(self):
        now = datetime.datetime.utcnow()
        res = sys_ping.run_pingcheck(self.gateway_ip)
        self.write_gatewaycheck(res["success"], now)

    def run_speedtest(self):
        self.s.get_best_server()
        self.s.download()
        self.s.upload(pre_allocate=False)
        res = self.s.results.dict()
        server = res["server"]
        #speedtest-cli's timestamp seems to return the same thing every time (?!) so use python's built in timestamp.
        #time = datetime.datetime.strptime(res["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ")
        time = datetime.datetime.utcnow()
        self.write_speedtest(res["download"], res["upload"], res["ping"], server["url"], server["name"], time)

    def write_gatewaycheck(self, is_online, time):
        pass

    def write_pingcheck(self, is_success, mean_ping, time):
        pass

    def write_speedtest(self, download, upload, ping, serverurl, servername, time):
        pass

    def write_failedpingcheck(self, time):
        pass

class PrintTester(Tester):
    def write_gatewaycheck(self, is_online, time):
        print (f"Gateway check produced status {str(is_online)} at time {str(time)}\n")
    def write_pingcheck(self, is_success, mean_ping, time):
        print (f"Ping check produced status {str(is_success)} at time {str(time)}, with a latency of {str(mean_ping)}\n")
    def write_speedtest(self, download, upload, ping, serverurl, servername, time):
        print (f"Speedtest ran with download of {download}, upload of {upload} and ping of {ping} with the server {servername} at {serverurl}, at time {time}.\n")
    def write_failedpingcheck(self, time):
        self.write_pingcheck(self, False, "Invalid", time)
