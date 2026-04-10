import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    result = sock.connect_ex(('127.0.0.1', 8000))
    if result == 0:
        print("Backend is responding on port 8000")
    else:
        print("Backend not responding. Connection code:", result)
finally:
    sock.close()
