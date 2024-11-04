# -*- coding: utf-8 -*-
# #Modell B
# wirking with mac
import os
import time
import subprocess
import argparse

def scan_network(ip_range, rate):
    command = f'nmap -T4 --min-rate={rate} {ip_range}'
    output = subprocess.check_output(command, shell=True, text=True)
    return output

def save_new_devices(new_devices, output_file):
    with open(output_file, 'a') as f:
        for device in new_devices:
            f.write(f'{device}\n')

def compare_and_notify(new_devices, old_devices):
    for device in new_devices:
        if device not in old_devices:
            print(f'Neuer Client gefunden: IP: {device.split()[0]}, MAC: {device.split()[1]}')

def print_active_devices(output):
    active_devices = []
    for line in output.splitlines():
        if 'MAC Address' in line and 'Nmap scan report' not in line:
            active_devices.append(line.strip())

    print("Aktive Clients:")
    for device in active_devices:
        print(device)

def print_open_ports(output):
    open_ports = []
    for line in output.splitlines():
        if 'Ports' in line:
            port_info = line.split()[3:]
            open_ports.append(port_info)

    print("Offene Ports:")
    for ports in open_ports:
        print(ports)

def main():
    parser = argparse.ArgumentParser(description='Netzwerk-Scan-Script')
    parser.add_argument('-d', '--devices', action='store_true', help='Aktive Clients anzeigen')
    parser.add_argument('-dv', '--devices-ports', action='store_true', help='Aktive Clients und offene Ports anzeigen')
    args = parser.parse_args()

    ip_range = '172.0.0.1/24'
    rate = '800'
    output_file = 'network_devices.txt'
    old_devices = set()

    while True:
        current_output = scan_network(ip_range, rate)
        new_devices = find_new_devices(current_output)
        save_new_devices(new_devices, output_file)
        old_devices.update(new_devices)

        if args.devices or args.devices_ports:
            if args.devices:
                print_active_devices(current_output)
            if args.devices_ports:
                print_open_ports(current_output)

        if input("Drücken Sie STRG+C, um das Skript zu beenden oder q, um das Skript nach 5 Minuten fortzusetzen: ").lower() in ['q', 'quit']:
            break

        time.sleep(300)  # 5 Minuten Wartezeit

def find_new_devices(output):
    new_devices = []
    for line in output.splitlines():
        if 'MAC Address' in line and 'Nmap scan report' not in line:
            new_devices.append(line.strip())
    return new_devices

if __name__ == "__main__":
    main()