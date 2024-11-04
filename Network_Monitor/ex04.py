# -*- coding: utf-8 -*-
import nmap
import time
import sys
import json

def scan_network():
    nm = nmap.PortScanner()
    nm.scan('172.0.0.1/24', arguments='-T4 --min-rate=800')
    return nm.all_hosts()

def save_to_file(hosts):
    with open('hosts.txt', 'w') as f:
        f.write(json.dumps(hosts))

def load_from_file():
    with open('hosts.txt', 'r') as f:
        return json.loads(f.read())

def compare_hosts(old_hosts, new_hosts):
    return [host for host in new_hosts if host not in old_hosts]

def main():
    try:
        old_hosts = load_from_file()
    except FileNotFoundError:
        old_hosts = []

    while True:
        new_hosts = scan_network()
        new_entries = compare_hosts(old_hosts, new_hosts)

        if new_entries:
            print(f"Neue Clients gefunden: {', '.join(new_entries)}")
            old_hosts = new_hosts
            save_to_file(old_hosts)

        time.sleep(300)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == '-d':
            hosts = load_from_file()
            print(f"Aktive Clients: {', '.join(hosts)}")
        elif sys.argv[1] == '-dv':
            nm = nmap.PortScanner()
            for host in load_from_file():
                res = nm.scan(host, arguments='-T4 --min-rate=800')
                print(f"Offene Ports für {host}: {res[host]['tcp'].keys()}")
    else:
        main()
