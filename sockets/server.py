import socket
import threading

class ChatServer:
    def __init__(self, host='127.0.0.1', port=8888):
        # Listas para objetos de clientes, nomes e mensagens
        self.clients = []
        self.usernames = []
        self.messages = []

        # Host e porta do servidor
        self.host = host
        self.port = port
        
        # Inicia a conexão do servidor e escuta
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
        
        print(f'Servidor iniciado na porta {self.port}...')

    def broadcast(self, message):
        # Mantém apenas as últimas 10 mensagens
        if len(self.messages) == 10:
            self.messages.pop()
        self.messages.append(message)
        
        # Manda mensagem para todos os clientes conectados
        for client in self.clients:
            client.send(message)

    def handle(self, client):
        while True:
            try:
                # Lida com a mensagem do cliente apos receber
                message = client.recv(1024)
                self.broadcast(message)
            except:
                # Em caso de erro excluir cliente da lista e remove o nome
                index = self.clients.index(client)
                self.clients.remove(client)
                client.close()

                username = self.usernames[index]
                self.usernames.remove(username)
                break

    def receive(self):
        while True:
            # Aceita o cliente e recebe o nome do usuário
            client, address = self.server.accept()
            username = client.recv(1024).decode('utf-8')
            
            # Adiciona o nome de usuário e objeto do cliente
            self.usernames.append(username)
            self.clients.append(client)
            
            # Avisa que foi conectado
            print(f'O cliente {username} se conectou!')
            client.send('Conectado ao servidor!'.encode('utf-8'))

            # Cria a thread para cada cliente
            threading.Thread(target=self.handle, args=(client,)).start()

    def run(self):
        self.receive()

if __name__ == '__main__':
    chat_server = ChatServer()
    chat_server.run()

