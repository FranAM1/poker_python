import socket

HOST = '127.0.0.1'  
PORT = 65432        

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    
    server_socket.listen()
    print("Servidor de poker en la terminal esperando conexiones...")
    
    conn, addr = server_socket.accept()
    
    with conn:
        print('Conexión establecida con', addr)
        
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print('Mensaje del cliente:', data.decode())
            
            # Enviar respuesta al cliente
            conn.sendall(b'Hola desde el servidor')