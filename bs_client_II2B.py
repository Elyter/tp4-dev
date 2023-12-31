import socket
import sys
import re
import logging
import os

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Emplacement du fichier de log du client
log_folder = '/var/log/bs_client/'

if not os.path.exists(log_folder):
    os.makedirs(log_folder)

log_file_path = os.path.join(log_folder, 'bs_client.log')

# Configuration du gestionnaire de fichiers pour les logs du client
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
logging.getLogger('').addHandler(file_handler)

# On définit la destination de la connexion
host = '10.37.128.5'  # IP du serveur
port = 13337               # Port choisi par le serveur

# Création de l'objet socket de type TCP (SOCK_STREAM)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connexion au serveur
    s.connect((host, port))
    # note : la double parenthèse n'est pas une erreur : on envoie un tuple à la fonction connect()

    logging.info(f"Connexion réussie à {host}:{port}.")

    # Envoi de data bidon
    input_data = input("Que veut tu envoyer au serveur : ")

    # Vérifier que l'entrée est une chaîne de caractères
    if not isinstance(input_data, str):
        raise TypeError("Erreur : Veuillez saisir une chaîne de caractères")

    # Vérifier que la chaîne contient soit "waf" soit "meo"
    if not re.match(r'^(waf|meo)$', input_data):
        raise ValueError("Erreur : La chaîne doit contenir soit 'waf' soit 'meo'")

    try:
        s.sendall(input_data.encode())
        logging.info(f"Message envoyé au serveur {host}:{port} : {input_data}")

        # On reçoit 1024 bytes qui contiennent peut-être une réponse du serveur
        data = s.recv(1024)
        logging.info(f"Réponse reçue du serveur {host}:{port} : {repr(data)}")

    except Exception as e:
        logging.error(f"Erreur lors de l'envoi des données : {e}")

except Exception as e:
    logging.error(f"Impossible de se connecter au serveur {host} sur le port {port} : {e}")

finally:
    # On libère le socket TCP
    s.close()

# Sortie du script
sys.exit(0)
