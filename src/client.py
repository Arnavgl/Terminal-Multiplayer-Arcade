import socket
import threading

HOST = 'localhost'
PORT = 5555

def receive_messages(sock):
    while True:
        try:
            msg = sock.recv(1024).decode()
            if not msg:
                break
            print(msg)
        except:
            print("Disconnected from server.")
            break

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))
    except:
        print("Unable to connect to server.")
        return

    threading.Thread(target=receive_messages, args=(client,), daemon=True).start()

    while True:
        try:
            msg = input()
            if msg:
                client.sendall(msg.encode())
        except KeyboardInterrupt:
            print("\nDisconnected.")
            break
        except Exception as e:
            print(f"[ERROR] {e}")
            break

    client.close()

if __name__ == "__main__":
    main()
