import socket
import threading
import sys

# Définir les paramètres du serveur
host = '127.0.0.1'  # Adresse IP locale
port = 5555         # Port d'écoute
fermeture_en_cours = False

# Créer le socket du serveur
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen()

print(f"Le serveur écoute sur {host}:{port}")

# Liste pour stocker les connexions clients
client_sockets = []
# Fonction pour gérer chaque client individuellement
def handle_client(client_socket):
    try:
        while True:
            # Logique pour gérer les messages du client
            data = client_socket.recv(1024).decode()
            if not data:
                break  # Le client s'est déconnecté
            print(f"Message reçu du client : {data}")

            # Envoyer le message à tous les clients
            for client in client_sockets:
                try:
                    client.send(data.encode())
                    print(f"Message envoyé au client : {data}")
                except:
                    # Gérer les erreurs d'envoi de message au client
                    pass
    except Exception as e:
        print(f"Erreur lors de la gestion du client : {e}")
    finally:
        client_sockets.remove(client_socket)  # Retirer le socket déconnecté de la liste
        client_socket.close()
        print("Client déconnecté.")



# Fonction pour écouter l'entrée de l'utilisateur
def listen_for_input():
    global fermeture_en_cours
    while True:
        user_input = input()
        if user_input.lower() == 'q' and not fermeture_en_cours:
            fermeture_en_cours = True
            print("Fermeture du serveur en cours...")

            # Envoyer un message de fermeture aux clients
            for client_socket in client_sockets:
                try:
                    client_socket.send("Fermeture du serveur".encode())
                    client_socket.close()
                except:
                    pass  # Ignorer les erreurs lors de la fermeture des sockets clients
            
            # Fermer le socket du serveur
            server_socket.close()
            sys.exit()


# Créer un thread pour écouter l'entrée de l'utilisateur
input_thread = threading.Thread(target=listen_for_input)
input_thread.start()

# Liste pour stocker les messages des clients
client_messages = []

# Fonction pour écouter les messages des clients
def listen_for_messages(client_socket):
    global fermeture_en_cours
    try:
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break  # Le client s'est déconnecté
            print(f"Message reçu du client : {data}")
            client_messages.append(data)
    except Exception as e:
        print(f"Erreur lors de l'écoute des messages du client : {e}")

# Créer un thread pour écouter les messages des clients
def start_listening_for_messages():
    global client_sockets
    while True:
        if fermeture_en_cours:
            break  # Ne pas écouter les messages pendant la fermeture

        for client_socket in client_sockets:
            listen_thread = threading.Thread(target=listen_for_messages, args=(client_socket,))
            listen_thread.start()

# Créer un thread pour écouter les messages des clients
message_thread = threading.Thread(target=start_listening_for_messages)
message_thread.start()

# Créer un thread pour envoyer les messages aux clients des qu'on en reçoit un
def start_sending_messages():
    global client_sockets
    global client_messages
    while True:
        if fermeture_en_cours:
            break  # Ne pas envoyer de messages pendant la fermeture

        if len(client_messages) > 0:
            message = client_messages.pop(0)
            for client_socket in client_sockets:
                try:
                    client_socket.send(message.encode())
                    print(f"Message envoyé au client : {message}")
                except:
                    # Gérer les erreurs d'envoi de message au client
                    pass
                
# Créer un thread pour envoyer les messages aux clients des qu'on en reçoit un
send_message_thread = threading.Thread(target=start_sending_messages)
send_message_thread.start()

# Accepter les connexions clientes et les gérer en parallèle
while True:
    if fermeture_en_cours:
        break  # Ne pas accepter de nouvelles connexions lors de la fermeture

    try:
        client_socket, addr = server_socket.accept()
        client_sockets.append(client_socket)
        print(f"Nouvelle connexion de {addr}")
        
        # Afficher le nombre de joueurs connectés
        print(f"Nombre de joueurs connectés : {len(client_sockets)}")

        #Le premier joueur à se connecter est le joueur 1
        if len(client_sockets) == 1:
            # Créer un thread pour gérer le client
            thread = threading.Thread(target=handle_client, args=(client_socket,))
            thread.start()
            client_socket.send("Joueur 1".encode())
        #Le second joueur à se connecter est le joueur 2
        elif len(client_sockets) == 2:
            # Créer un thread pour gérer le client
            thread = threading.Thread(target=handle_client, args=(client_socket,))
            thread.start()
            client_socket.send("Joueur 2".encode())
        # Le troisième joueur à se connecter est le joueur 3
        elif len(client_sockets) == 3:
            thread = threading.Thread(target=handle_client, args=(client_socket,))
            thread.start()
            client_socket.send("Joueur 3".encode())
        # Le quatrième joueur à se connecter est le joueur 4
        elif len(client_sockets) == 4:
            thread = threading.Thread(target=handle_client, args=(client_socket,))
            thread.start()
            client_socket.send("Joueur 4".encode())
        # Le reste des joueurs se font refuser la connexion
        else:
            client_socket.send("Refus".encode())
            client_socket.close()
    except Exception as e:
        # Gérer les erreurs d'acceptation de la connexion pendant la fermeture
        if fermeture_en_cours:
            break
        else:
            print(f"Erreur lors de l'acceptation de la connexion : {e}")

