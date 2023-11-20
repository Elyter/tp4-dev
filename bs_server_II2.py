import socket
import sys
import signal
import threading
import time
import logging
from logging.handlers import TimedRotatingFileHandler

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
log_handler = TimedRotatingFileHandler('/var/log/bs_server/bs_server.log', when='midnight', interval=1, backupCount=7)
log_handler.setLevel(logging.INFO)
log_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
logging.getLogger('').addHandler(log_handler)

host = ''
port = 13337
if len(sys.argv) > 1:
    if sys.argv[1] == '-h' or sys.argv[1] == '--help':
        print("Usage : python3 bs_server_II1.py [OPTION] [ARGUMENT]\n\n\t-h, --help \t\t Affiche l'aide\n\t-p, --port \t\t Spécifie le port sur lequel le serveur va écouter\n\n")
        sys.exit(0)
    # On choisit une IP et un port où on va écouter
 # string vide signifie, dans ce conetxte, toutes les IPs de la machine
    if sys.argv[1] == '-p' or sys.argv[1] == '--port':
        if 0 <= int(sys.argv[2]) <= 65535:
            if 0 <= int(sys.argv[2]) <= 1024:
                raise ValueError("ERROR Le port spécifié est un port privilégié. Spécifiez un port au dessus de 1024.")
                sys.exit(2)
            else:
                port = int(sys.argv[2])
                logging.info("Lancement du serveur")
                logging.info(f"Le serveur tourne sur {host}:{port}")
        else:
            raise ValueError("ERROR Le port spécifié n'est pas un port possible (de 0 à 65535).")
            sys.exit(1)
    else:
        port = 13337 # port choisi arbitrairement

# On crée un objet socket
# SOCK_STREAM c'est pour créer un socket TCP (pas UDP donc)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# On demande à notre programme de se bind sur notre portd
s.bind((host, port))  

# Place le programme en mode écoute derrière le port auquel il s'est bind
s.listen(1)


# Petite boucle infinie (bah oui c'est un serveur)
# A chaque itération la boucle reçoit des données et les traite
while True:
    try:
        conn, addr = s.accept()
        logging.info(f"Un client <{addr[0]}> s'est connecté.")
        while True:
            data = conn.recv(1024)
            if not data:
                break

            logging.info(f"Message reçu d'un client <{addr[0]}> : {message}")

            if b'meo' in data:
                response = b'Meo a toi confrere.'
                conn.send(response)
                logging.info(f"Message envoyé au client <{addr[0]}> : {response.decode('utf-8')}")
            elif b'waf' in data:
                response = b'Ptdr t ki ?'
                conn.send(response)
                logging.info(f"Message envoyé au client <{addr[0]}> : {response.decode('utf-8')}")
            else:
                response = b'Mes respects humble humain.'
                conn.send(response)
                logging.info(f"Message envoyé au client <{addr[0]}> : {response.decode('utf-8')}")

    except socket.error:
        logging.error("Erreur lors de la connexion.")
        break

def check_no_clients():
    while True:
        time.sleep(60)
        if not clients_connected:
            logging.warning("Aucun client depuis plus d'une minute.")

threading.Thread(target=check_no_clients).start()

def signal_handler(sig, frame):
    logging.info("Arrêt du serveur.")
    conn.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
