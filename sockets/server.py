import socket
import threading

# Configurações do servidor
HOST = '127.0.0.1'  # Use o IP do servidor
PORT = 12345

# Criação do socket do servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

# Lista para armazenar conexões de clientes
client_connections = []

# Função para enviar mensagens para todos os clientes
def broadcast(message, client_socket):
    for client in client_connections:
        if client != client_socket:
            try:
                client.send(message)
            except:
                # Caso a conexão com o cliente tenha falhado, remova a conexão
                remove_client(client)

# Função para remover um cliente da lista de conexões
def remove_client(client_socket):
    if client_socket in client_connections:
        client_connections.remove(client_socket)

# Função para lidar com as mensagens recebidas de um cliente
def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                remove_client(client_socket)
                break
            broadcast(message, client_socket)
        except:
            continue

# Função principal para aceitar conexões e lidar com os clientes
def main_server():
    while True:
        client_socket, client_address = server_socket.accept()
        
        username = client_socket.recv(1024).decode('utf-8')
        welcome_message = f"Bem-vindo, {username}! Digire uma mensagem para começar.\n" + '-' * 100 + '\n' 
        client_socket.send(welcome_message.encode('utf-8'))
        client_connections.append(client_socket)

        print(f"Conexão estabelecida com {client_address} como {username}")
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    main_server()

