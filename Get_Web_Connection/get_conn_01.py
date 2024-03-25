import time, keyboard, os
import urllib.request
import urllib.error
from colorama import Fore, Style


def _close():
    try:
        if keyboard.is_pressed('ctrl') and keyboard.is_pressed('q'):
            print(Fore.LIGHTRED_EX + "[+] Process is closed")
            Style.RESET_ALL
            exit(0)
    except KeyboardInterrupt:
        pass
def connect_site(url, timestamp):
    print(Fore.LIGHTBLUE_EX + f"[+] Try Connection to {url}")
    _close()
    conn = urllib.request.urlopen('https://' + url)
    _close()
    print(Fore.GREEN + f"[+] Connection was successful, with response {conn.code}")
    _close()
    return conn
def response_handling(e, url):
    timestamp = time.strftime("%Y.%m.%d %H:%M:%S", time.localtime())
    if e.code >= 200 and e.code < 300:
        msg = f'{timestamp}\tSeccessful code {e}\tURL:\t{ {url} }\n'
        print(Fore.GREEN, msg)
        write_status(url, msg)
        _close()
    elif e.code >= 300 and e.code < 400:
        msg = f'{timestamp}\tHTTPError:\t{e}\tURL: {url}\n'
        print(Fore.YELLOW, msg)
        write_status(url, msg)
        _close()
    elif e.code >= 400 and e.code < 500:
        msg = f'{timestamp}\tClient error: {e}\tURL: {url}\n'
        print(Fore.RED, msg)
        write_status(url, msg)
        _close()
    else:
        msg = f'{timestamp}\tServer error: {e}\tURL: {url}\n'
        print(Fore.RED, msg)
        write_status(url, msg)
        _close()
def uptime(url):
    try:
        timestamp = time.strftime("%Y.%m.%d %H:%M:%S", time.localtime())
        conn = connect_site(url, timestamp)
        _close()
    except urllib.error.HTTPError as e:
        # Email admin / log
        response_handling(e, url)
        _close()
    except urllib.error.URLError as e:
        # Email admin / log
        msg = f'{timestamp}\tURLError: {e.reason}\tURL: {url}\n'
        print(Fore.RED, msg)
        write_status(url, msg)
        _close()
    else:
        # Website is up
        msg = f'{timestamp}\tSeccessful code {conn.code}\tURL: \t{url}\n'
        print(msg)
        write_status(url, msg)
        _close()
    Style.RESET_ALL


def write_status(url, msg):
    timestamp = time.strftime("%Y.%m.%d", time.localtime())
    uri = url.replace('/', '_').replace('\\', '_')
    filename = f"{timestamp}_{uri}.log"
    if not os.path.exists('log'):
        os.mkdir('log')
    if not os.path.exists('log/' + filename):
        with open('log/' + filename, 'w', encoding='utf-8') as f:
            f.write(msg)
    with open('log/' + filename, 'a', encoding='utf-8') as f:
        f.write(msg)
    f.close()

def main():

    urls = ['exploit-db.com', 'example.com/404', 'yandex.ru', 'sploitus.com']
    while True:
        for url in urls:
            uptime(url)
        time.sleep(15.5)

if __name__ == '__main__':
    main()