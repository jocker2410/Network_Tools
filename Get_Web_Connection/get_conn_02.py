import os, time, keyboard, requests
from colorama import Fore, Style

def _close():
    try:
        if keyboard.is_pressed('ctrl') and keyboard.is_pressed('q'):
            print(Fore.LIGHTRED_EX + "[+] Process is closed")
            Style.RESET_ALL
            exit(0)
    except KeyboardInterrupt:
        pass

def connect_site(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'
    }
    print(Fore.LIGHTBLUE_EX + f"[+] Try Connection to {url}")
    _close()
    response = requests.get(f'https://{url}', headers=headers)
    _close()
    if response.status_code >= 200 and response.status_code < 300:
        print(Fore.GREEN + f"[+] Connection was successful, with response {response.status_code}")
    else:
        print(Fore.YELLOW + f"[+] Unexpected response code: {response.status_code}")
    _close()
    return response

def response_handling(url, response):
    timestamp = time.strftime("%Y.%m.%d %H:%M:%S", time.localtime())
    if response.status_code >= 200 and response.status_code < 300:
        msg = f"{timestamp}\tSuccessful code {response.status_code}\tURL:\t{url}\n"
        print(Fore.GREEN, msg)
    elif response.status_code >= 300 and response.status_code < 400:
        msg = f"{timestamp}\tHTTPError:\t{response.status_code}\tURL: {url}\n"
        print(Fore.YELLOW, msg)
    elif response.status_code >= 400 and response.status_code < 500:
        msg = f"{timestamp}\tClient error: {response.status_code}\tURL: {url}\n"
        print(Fore.RED, msg)
    else:
        msg = f"{timestamp}\tServer error: {response.status_code}\tURL: {url}\n"
        print(Fore.RED, msg)
    write_status(url, msg)

def uptime(url):
    try:
        response = connect_site(url)
        _close()
    except requests.exceptions.RequestException as e:
        # Email admin / log (handle exceptions more specifically if needed)
        msg = f"{time.strftime('%Y.%m.%d %H:%M:%S', time.localtime())}\tError: {e}\tURL: {url}\n"
        print(Fore.RED, msg)
        write_status(url, msg)
        _close()
    else:
        response_handling(url, response)
        _close()
    Style.RESET_ALL

def write_status(url, msg):
    timestamp = time.strftime("%Y.%m.%d", time.localtime())
    uri = url.replace('/', '_').replace('\\', '_')
    filename = f"{timestamp}_{uri}.log"
    if not os.path.exists('log'):
        os.mkdir('log')
    with open(f'log/{filename}', 'a', encoding='utf-8') as f:
        f.write(msg)

def main():
    urls = ['exploit-db.com', 'example.com/404', 'yandex.ru', 'sploitus.com']
    while True:
        for url in urls:
            uptime(url)
        time.sleep(8.5)

if __name__ == '__main__':
    main()
