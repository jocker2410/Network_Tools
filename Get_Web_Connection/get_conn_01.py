import time
import urllib.request
import urllib.error

def uptime_bot(url):
    while True:
        try:
            conn = urllib.request.urlopen(url)

        except urllib.error.HTTPError as e:
            # Email admin / log
            print(f'HTTPError: {e.code} for {url}')
        except urllib.error.URLError as e:
            # Email admin / log
            print(f'URLError: {e.reason} for {url}\nCheck your Internet Connection')
        else:
            # Website is up
            print(f'{url} is up, status {conn.code}')

def main():
    url = 'https://www.ifconfig.io/'
    urls = ['imkerei-herzog.de']
    uptime_bot(url)
    time.sleep(1)

if __name__ == '__main__':
    main()