import socket

# Configuración del cliente
HOST = '127.0.0.1' 
PORT = 65432        

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    
    while True:
        # Enviar mensaje al servidor
        message = input("Mensaje para el servidor: ")
        client_socket.sendall(message.encode())
        
        # Recibir respuesta del servidor
        data = client_socket.recv(1024)
        print('Respuesta del servidor:', data.decode())