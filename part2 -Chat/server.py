import socket
import threading

# Connection settings
HOST = '127.0.0.1'
PORT = 5555

# Dictionary to store connected clients: {client_name: client_socket}
clients = {}

def handle_client(client_socket):
    name = ""
    try:
        # Receive client name upon connection
        name = client_socket.recv(1024).decode('utf-8')
        clients[name] = client_socket
        print(f"[+] Connected: {name}")
        
        while True:
            # Receive message
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            
            # Check if message format is "DEST:MESSAGE"
            if ':' in message:
                target_name, msg_content = message.split(':', 1)
                if target_name in clients:
                    # Send to target
                    clients[target_name].send(f"From {name}: {msg_content}".encode('utf-8'))
                else:
                    client_socket.send(f"User {target_name} not found.".encode('utf-8'))
            else:
                client_socket.send("Error: Use format 'NAME:MESSAGE'".encode('utf-8'))
                
    except Exception as e:
        print(f"Error with {name}: {e}")
    finally:
        # Disconnect
        if name in clients:
            del clients[name]
        client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[*] Server listening on {HOST}:{PORT}")
    
    while True:
        client, addr = server.accept()
        threading.Thread(target=handle_client, args=(client,)).start()

if __name__ == "__main__":
    start_server()