import socket
import threading
from cryptography.fernet import Fernet
import datetime

# Key for encryption (this should be kept secret and consistent between server and client)
key = Fernet.generate_key()
#key = input("Enter the encryption key: ").encode()
cipher = Fernet(key)
print(f"Encryption key (use this for client too): {key}")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 5555))
server.listen()

rooms = {}



def handle_client(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            decrypted_msg = cipher.decrypt(message.encode()).decode()

            room_name, msg = decrypted_msg.split("|", 1)
            log_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"[{log_time}] Room: {room_name} - {msg}")

            for c in rooms.get(room_name, []):
                if c != client:
                    c.send(cipher.encrypt(f"{room_name}|{msg}".encode()))

        except:
            for room, clients in rooms.items():
                if client in clients:
                    clients.remove(client)
                    break
            client.close()
            break

while True:
    client, address = server.accept()
    room_name = cipher.decrypt(client.recv(1024)).decode()
    
    if room_name not in rooms:
        rooms[room_name] = []
    rooms[room_name].append(client)

    client_thread = threading.Thread(target=handle_client, args=(client,))
    client_thread.start()
