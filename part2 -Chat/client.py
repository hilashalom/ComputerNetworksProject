import socket
import threading

HOST = '127.0.0.1'
PORT = 5555

def receive_messages(sock):
    while True:
        try:
            msg = sock.recv(1024).decode('utf-8')
            if msg:
                print(f"\n{msg}\nYour message: ", end='')
        except:
            print("Disconnected from server.")
            break

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    
    # Enter username
    name = input("Enter your username: ")
    client.send(name.encode('utf-8'))
    
    # Start listening thread
    threading.Thread(target=receive_messages, args=(client,), daemon=True).start()
    
    print("To send message use format: TARGET:MESSAGE (e.g., Bob:Hello)")
    
    while True:
        msg = input("Your message: ")
        if msg == 'quit':
            break
        client.send(msg.encode('utf-8'))
    
    client.close()

if __name__ == "__main__":
    start_client()