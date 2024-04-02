import socket
import threading
import sys


host = "127.0.0.1"                                         
port = 5555                                                 
fermeture_en_cours = False

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen()

print(f"Le serveur écoute sur {host}:{port}")

client_sockets = []

client_messages = []

def handle_client(client_socket):
    try:
        while True:
            data = client_socket.recv(10000000).decode()
            if not data:
                break 
            print(f"Message reçu du client : {data}")

            for client in client_sockets:
                try:
                    client.send(data.encode())
                    print(f"Message envoyé au client : {data}")
                except:
                    pass
    except Exception as e:
        print(f"Erreur lors de la gestion du client : {e}")
    finally:
        client_sockets.remove(client_socket)  
        client_socket.close()
        print("Client déconnecté.")

def listen_for_input():
    global fermeture_en_cours
    while True:
        user_input = input()
        if user_input.lower() == 'q' and not fermeture_en_cours:
            fermeture_en_cours = True
            print("Fermeture du serveur en cours...")

            for client_socket in client_sockets:
                try:
                    client_socket.send("Fermeture du serveur".encode())
                    client_socket.close()
                except:
                    pass 
            
            server_socket.close()
            sys.exit()
        elif user_input.lower() == 'c':
            print(f"Nombre de clients connectés : {len(client_sockets)}")


input_thread = threading.Thread(target=listen_for_input)
input_thread.start()

client_messages = []

def listen_for_messages(client_socket):
    global fermeture_en_cours
    try:
        while True:
            data = client_socket.recv(100000).decode()
            if not data:
                break 
            print(f"Message reçu du client : {data}")
            client_messages.append(data)
    except Exception as e:
        print(f"Erreur lors de l'écoute des messages du client : {e}")

def start_listening_for_messages():
    global client_sockets
    while True:
        if fermeture_en_cours:
            break 

        for client_socket in client_sockets:
            listen_thread = threading.Thread(target=listen_for_messages, args=(client_socket,))
            listen_thread.start()

message_thread = threading.Thread(target=start_listening_for_messages)
message_thread.start()

def start_sending_messages():
    global client_sockets
    global client_messages
    while True:
        if fermeture_en_cours:
            break 

        if len(client_messages) > 0:
            message = client_messages.pop(0)
            for client_socket in client_sockets:
                try:
                    client_socket.send(message.encode())
                    print(f"Message envoyé au client : {message}")
                except:
                    pass
                
send_message_thread = threading.Thread(target=start_sending_messages)
send_message_thread.start()

while True:
    if fermeture_en_cours:
        input_thread.join() 
        message_thread.join()
        send_message_thread.join()
        break

    try:
        client_socket, addr = server_socket.accept()
        client_sockets.append(client_socket)
        print(f"Nouvelle connexion de {addr}")
        
        print(f"Nombre de joueurs connectés : {len(client_sockets)}")

        if len(client_sockets) == 1:
            thread = threading.Thread(target=handle_client, args=(client_socket,))
            thread.start()
            client_socket.send("1".encode())
            
        elif len(client_sockets) == 2:
            thread = threading.Thread(target=handle_client, args=(client_socket,))
            thread.start()
            client_socket.send("2".encode())
            
        elif len(client_sockets) == 3:
            thread = threading.Thread(target=handle_client, args=(client_socket,))
            thread.start()
            client_socket.send("3".encode())
            
        elif len(client_sockets) == 4:
            thread = threading.Thread(target=handle_client, args=(client_socket,))
            thread.start()
            client_socket.send("4".encode())
        else:
            client_socket.send("Refus".encode())
            client_socket.close()
            
    except Exception as e:
        if fermeture_en_cours:
            input_thread.join() 
            message_thread.join()
            send_message_thread.join()
            break
        else:
            print(f"Erreur lors de l'acceptation de la connexion : {e}")

