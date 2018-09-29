import platform
import subprocess
import re
import statistics

def run_pingcheck(ip, count=4, retries=1):
    pings = []
    for i in range(0, count):
        res = check_ping(ip)
        if (not res["success"]) and (retries > 0):
            return run_pingcheck(ip, count, retries-1)
        elif not res["success"]:
            return {"success": False}
        else:
            pings.append(res["time"])
    midpings = list(pings)
    midpings.remove(max(midpings))
    midpings.remove(min(midpings))
    return {
        "success": True,
        "latencies": pings,
        "mean_ping": statistics.mean(midpings)
        }

def check_ping(ip):
    os = platform.system()
    if os == "Windows":
        return check_ping_win(str(ip))
    elif os == "Linux":
        return check_ping_linux(str(ip))
    else:
        return {
            "success": False,
            "error_code": -1,
            "error_msg": "OS not supported"
            }

def check_ping_win(ip_str):
    command = ["ping", "-n", "1", ip_str]
    pingproc = subprocess.run(command, stdout=subprocess.PIPE)
    if pingproc.returncode == 0:
        #Ping was successful
        com_str = str(pingproc.stdout)
        regex_str = f"Reply from {re.escape(ip_str)}: bytes=([0-9]+) time[=|\<]([0-9]+)ms TTL=([0-9]+)"
        p = re.compile(regex_str)
        match = p.search(com_str)
        return {
            "success": True,
            "time": float(match.group(2)),
            "ttl": match.group(1)
            }
    else:
        return {
            "success": False,
            "error_code": pingproc.returncode,
            "error_msg": pingproc.stdout.decode("utf-8")
            }

def check_ping_linux(ip_str):
    command = ["ping", "-c", "1", ip_str]
    pingproc = subprocess.run(command, stdout=subprocess.PIPE)
    if pingproc.returncode == 0:
        #Ping was successful
        com_str = str(pingproc.stdout)
        regex_str = f"([0-9]+) bytes from {re.escape(ip_str)}: icmp_seq=1 ttl=([0-9]+) time[=|\<](\d*\.\d+|\d+) ms"
        p = re.compile(regex_str)
        match = p.search(com_str)
        return {
            "success": True,
            "time": float(match.group(3)),
            "ttl": match.group(2)
            }
    else:
        return {
            "success": False,
            "error_code": pingproc.returncode,
            "error_msg": pingproc.stdout.decode("utf-8")
            }
