# Modell A
# Neuen Host nicht bemerkt
import os
import time
import sys
import nmap
from datetime import datetime

nm = nmap.PortScanner()
def scan_network():
    print("Scanning network, please wait...")
    nm.scan(hosts='172.0.0.1/24', arguments='-T4 --min-rate=800')

    return nm.all_hosts()

def print_network_info(nm, host, verbose):
    host_name = nm[host].hostname()
    print(f'Host : {host} {host_name}')
    print(f'State : {nm[host].state()}')

    for proto in nm[host].all_protocols():
        print('----------')
        print(f'Protocol : {proto}')

        lport = list(nm[host][proto].keys())
        lport.sort()

        for port in lport:
            result = nm[host][proto][port]
            print(f'port : {port} {result["name"]}\t{result["state"]}')

            if verbose:
                for key in result:
                    if key != "state":
                        print(f'{key} : {result[key]}')
    print(f"\n\n")

def main():
    if "-d" in sys.argv or "-dv" in sys.argv:
        verbose = "-dv" in sys.argv
        current_hosts = scan_network()

        print("\nActive clients:")
        for host in current_hosts:
            print_network_info(nm, host, verbose)

        return

    known_hosts = set()
    if os.path.exists("known_hosts.txt"):
        with open("known_hosts.txt") as f:
            known_hosts = set(line.strip() for line in f)

    while True:
        try:
            current_hosts = set(scan_network())
            new_hosts = current_hosts - known_hosts

            if new_hosts:
                print(f"\nNew clients found at {datetime.now()}:")

                for host in new_hosts:
                    print_network_info(nm, host, False)

                print("\nUpdating known_hosts...")
                known_hosts = current_hosts

                with open("known_hosts.txt", "w") as f:
                    for host in known_hosts:
                        f.write(f"{host}\n")

            else:
                print("No new clients found.")

            time.sleep(2)

        except KeyboardInterrupt:
            print("\nExiting...")
            break

if __name__ == "__main__":
    main()