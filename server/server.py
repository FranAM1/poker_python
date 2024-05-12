import socket

# Configuración del servidor
HOST = '127.0.0.1'  # Dirección IP del servidor (localhost)
PORT = 65432        # Puerto para escuchar conexiones

# Crear un socket TCP/IP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    # Vincular el socket a la dirección y puerto especificados
    server_socket.bind((HOST, PORT))
    
    # Escuchar conexiones entrantes
    server_socket.listen()
    print("Servidor de poker en la terminal esperando conexiones...")
    
    # Aceptar la primera conexión entrante
    conn, addr = server_socket.accept()
    
    with conn:
        print('Conexión establecida con', addr)
        
        while True:
            # Recibir datos del cliente
            data = conn.recv(1024)
            if not data:
                break
            print('Mensaje del cliente:', data.decode())
            
            # Enviar respuesta al cliente
            conn.sendall(b'Hola desde el servidor')