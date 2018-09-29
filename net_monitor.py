import net_tester
import datetime
import time
import threading
import ipaddress

class NetMonitor:
    def __init__(self, tester, gatewaycheck_delta, pingcheck_delta, speedcheck_delta):
        self.tester = tester
        self.pingcheck_delta = pingcheck_delta
        self.gatewaycheck_delta = gatewaycheck_delta
        self.speedcheck_delta = speedcheck_delta
        
        now = datetime.datetime.now()
        self.next_pingcheck = now
        self.next_gatewaycheck = now
        self.next_speedcheck = now

    def start_monitoring(self):
        while(True):
            now = datetime.datetime.now()
            if now >= self.next_pingcheck:
                self.next_pingcheck = now + self.pingcheck_delta
                self.run_pingcheck()
            elif now >= self.next_gatewaycheck:
                self.next_gatewaycheck = now + self.gatewaycheck_delta
                self.run_gatewaycheck()
            elif now >= self.next_speedcheck:
                self.next_speedcheck = now + self.speedcheck_delta
                self.run_speedcheck()
            else:
                time.sleep(1)
                
    def run_pingcheck(self):
        now = datetime.datetime.now()
        t = threading.Thread(target = self.tester.run_pingcheck, name=f"Pingcheck-{now}")
        t.daemon = True
        t.start()

    def run_gatewaycheck(self):
        now = datetime.datetime.now()
        t = threading.Thread(target = self.tester.run_gatewaycheck, name=f"Gatewaycheck-{now}")
        t.daemon = True
        t.start()

    def run_speedcheck(self):
        now = datetime.datetime.now()
        t = threading.Thread(target = self.tester.run_speedtest, name=f"Speedtest-{now}")
        t.daemon = True
        t.start()
