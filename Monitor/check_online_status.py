# -*- coding: utf-8 -*-
#   File:       check_online_status.py
#   Created by: jocker2410
#   Created:    2024/05/23 17:19:03 by jocker2410
#   Updated:    2024/04/08 17:20:27 by jocker2410

#  This tool checks whether a system can be reached via port 20 and writes the status of the system to a log file.
import socket
import time
import datetime

class PingChecker:
    def __init__(self, ip):
        self.ip = ip
        self.log_file = "session_log.txt"
        self.online_status = False

    def ping(self):
        try:
            # Check connection on port 22
            socket.create_connection((self.ip, 22), timeout=1)
            return True
        except OSError:
            return False

    def log(self, message):
        with open(self.log_file, "a") as f:
            f.write(f"{datetime.datetime.now()} - {message}\n")

    def check_status(self):
        status = self.ping()
        if status and not self.online_status:
            print(f"{self.ip} is online")
            self.log(f"{self.ip} ist online")
        elif not status and self.online_status:
            print(f"{self.ip} is offline")
            self.log(f"{self.ip} is offline")
        else:
            print(f"{self.ip} is {'online' if status else 'offline'}")

        self.online_status = status
        return status

def main(ip):
    checker = PingChecker(ip)
    while True:
        if not checker.check_status():
            # sleep for 120 sec
            time.sleep(120)
        else:
            time.sleep(1)

if __name__ == "__main__":
    ip = "127.0.0.2"
    main(ip)
