import socket

# On choisit une IP et un port où on va écouter
host = '' # string vide signifie, dans ce conetxte, toutes les IPs de la machine
port = 13337 # port choisi arbitrairement

# On crée un objet socket
# SOCK_STREAM c'est pour créer un socket TCP (pas UDP donc)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# On demande à notre programme de se bind sur notre port
s.bind((host, port))  

# Place le programme en mode écoute derrière le port auquel il s'est bind
s.listen(1)


# Petite boucle infinie (bah oui c'est un serveur)
# A chaque itération la boucle reçoit des données et les traite
while True:

    try:
        # On reçoit 1024 bytes de données
        data = conn.recv(1024)

        # Si on a rien reçu, on continue
        if data:
            print(f"Le client {addr} a envoyé {data}")

        # On répond au client un truc
        conn, addr = s.accept()
        print("Un client vient de se co et son IP c'est", addr)
        conn.send(b'Welcome to the server! You are now connected.')  # Envoie un message de succès au client
        while True:
            data = conn.recv(1024)
            if not data:
                break

            print(f"Le client {addr} a envoyé {data}")
            if b'meo' in data:
                conn.send(b'Meo a toi confrere.')
            elif b'waf' in data:
                conn.send(b'Ptdr t ki ?')
            else:
                conn.send(b'Mes respects humble humain.')
                
    except socket.error:
        print("Error Occured.")
        break

# On ferme proprement la connexion TCP
conn.close()
