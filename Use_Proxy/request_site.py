# Importieren der erforderlichen Module
import requests
import datetime
import re
import socks
import socket

# Facebook onion URL for testing
url = "facebookwkhpilnemxj7asaniu7vnjjbiltxjqhye3mhbshg7kx5tfyd.onion"

# DuckDuckGo

# Erstellen einer Sitzung mit dem Tor-Proxy
session = requests.session()

# Verwenden von SOCKS5 für den SOCKS-Typ
session.proxies = {
    "http": socks.SOCKS5,
    "https": socks.SOCKS5,
}

# Versuchen, die URL abzurufen
try:
    response = session.get(url)

    # Überprüfen, ob die Anfrage erfolgreich war
    if response.status_code == 200:
        # Extrahieren des Quellcodes der Seite
        source = response.text

        # Extrahieren des Titels der Seite
        try:
            title = re.search("<title>(.*?)</title>", source).group(1)
        except Exception as e:
            print(f"Fehler beim Extrahieren des Titels: {e}")
            title = "Kein Titel gefunden"

        # Erstellen eines Zeitstempels
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Erstellen eines Dateinamens mit dem Titel und dem Zeitstempel
        filename = f"{title}_{timestamp}.html"

        # Speichern des Quellcodes in einer Datei
        with open(filename, "w") as file:
            file.write(source)

        # Ausgeben einer Erfolgsmeldung
        print(f"Die Seite {url} ist erreichbar. Der Quellcode wurde in {filename} gespeichert.")
    else:
        # Ausgeben einer Fehlermeldung
        print(f"Die Seite {url} ist nicht erreichbar. Der Statuscode ist {response.status_code}.")

except Exception as e:
    # Ausgeben einer Ausnahme
    print(f"Es ist ein Fehler aufgetreten: {e}")
