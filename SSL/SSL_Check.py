#   File:       SSL_Check.py
#   Created by: jocker2410
#   Created:    2023/05/23 14:05:24 by jocker2410
#   Updated:    2024/03/24 15:25:14 by jocker2410

import os, ssl, socket
from datetime import datetime
from colorama import Fore, Style

class GetSSL:
    def __init__(self, websites):
        self.websites = websites

    def _get_cert_info(self, website):
        try:
            context = ssl.create_default_context()
            conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=website)
            conn.connect((website, 443))
            cert = conn.getpeercert()
            conn.close()
            cert_not_after = datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")
            exp_days = (cert_not_after - datetime.now()).days

            return cert_not_after, exp_days

        except (ssl.CertificateError, socket.error) as e:
            return None, None

    def _p_green(self, msg):
        print(f"{Fore.GREEN}[+] {msg}{Style.RESET_ALL}")

    def _p_red(self, msg):
        print(f"{Fore.RED}[+] {msg}{Style.RESET_ALL}")

    def _p_yellow(self, msg):
        print(f"{Fore.YELLOW}[+] {msg}{Style.RESET_ALL}")

    def check_ssl(self):
        print("")
        for website in self.websites:
            cert_not_after, exp_days = self._get_cert_info(website)
            self._p_yellow(f"[!] Check Site \t-->\t\t{website}")

            if cert_not_after and exp_days:
                self._p_green(f"Vakud until: \t\t\t{cert_not_after}")
                self._p_green(f"Valid for: \t\t\t\t{exp_days} days")

            else:
                self._p_red("[-] Certificate could not be verified!")
            print()
def clear_screen():
  if os.name == "nt":
    os.system("cls")
  else:
    os.system("clear")

def main():
    websites = ["vpn.phalanx-it.de"]
    clear_screen()
    ssl_checker = GetSSL(websites)
    ssl_checker.check_ssl()

if __name__ == '__main__':
    main()