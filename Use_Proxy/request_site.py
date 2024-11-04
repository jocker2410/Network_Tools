import requests, json
from colorama import Fore, Style
url = "http://libraryfyuybp7oyidyya3ah5xvwgyx6weauoini7zyz555litmmumad.onion"

def get_tor_session():
    session = requests.session()
    # for tor i use 9050 port
    session.proxies = {'http':  'socks5://127.0.0.1:9050',
                       'https': 'socks5://127.0.0.1:9050'}
    return session
def try_Tor(session):
    # curent ip
    ip_check = 'http://httpbin.org/ip'
    ori_ip = json.loads(requests.get(ip_check).text)
    print(Fore.GREEN + f"[+] Curent IP: {ori_ip['origin']}")
    # tor ip
    tor_ip = json.loads(session.get(ip_check).text)
    print(Fore.GREEN + f"[+] Tor service is up\n[+] Tor IP: {tor_ip['origin']}")

def req_site(session, url):
    data = session.get(url)
    print(data.text)

def main():

    # print hidden ip
    #try_Tor(get_tor_session())

    req_site(get_tor_session(), url)
    print(Style.RESET_ALL + "down")
    #print(session.get(url).text)


if __name__ =='__main__':
    main()
