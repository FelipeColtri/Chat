import grpc
import chat_pb2
import chat_pb2_grpc
import threading
import tkinter as tk
from tkinter import scrolledtext, Entry, Button, simpledialog

class ChatClient:
    def __init__(self):
        # Obter o host e o nome de usuário 
        self.host = simpledialog.askstring('Conexão ao Servidor', 'Digite o IP do servidor:\n(Deixar em branco = localhost)')

        if self.host == '' or self.host == '172.0.0.1':
            self.host = 'localhost'

        while True:
            self.username = simpledialog.askstring('Conexão ao Servidor', 'Digite seu nome de usuário:\n (No mínimo 3 letras)')
            if len(self.username) >= 3:
                break

        # Iniciando o gRPC no cliente
        self.channel = grpc.insecure_channel(f'{self.host}:50051')
        self.stub = chat_pb2_grpc.ChatServiceStub(self.channel)
        
        # Cria a tela principal
        self.window = tk.Tk()
        self.window.title(f'Chat de {self.username}')

        # Caixa de texto onde estarão as mensagens
        self.chat_box = scrolledtext.ScrolledText(self.window, state='disabled')
        self.chat_box.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Campo de escrever a mensagem 
        self.message_entry = Entry(self.window)
        self.message_entry.config(font=('Arial', 16))
        self.message_entry.bind('<Return>', lambda event=None : self.send_message())
        self.message_entry.focus()
        self.message_entry.grid(row=1, column=0, padx=10, pady=10, sticky='ew')
        
        # Botão de enviar a mensagem
        self.send_button = Button(self.window, text='Enviar', command=self.send_message)
        self.send_button.config(font=('Arial', 16, 'bold'))
        self.send_button.grid(row=1, column=1, padx=10, pady=10, sticky='ew')

        # Posição dos elementos
        self.window.columnconfigure(0, weight=4)
        self.window.columnconfigure(1, weight=1)

        # Cria a thread para receber as mensagens 
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def send_message(self):
        # Pega a mensagens no campo de entrada com TRIM
        message = self.message_entry.get().strip()

        # Se não for em branco mande para o servidor
        if len(message):
            response = self.stub.SendMessage(chat_pb2.MessageRequest(username=self.username, message=message))
        
        # Limpar e focalizar na caixa de entrada
        self.message_entry.delete(0, tk.END)
        self.message_entry.focus()

    def update_messages(self, user, msg):
        # Cor vermelha se é a própria mensagem, senão azul
        color = '#0000FF'

        if user == self.username:
            color = '#FF0000'
            
        # Coloca a mensagem na caixa de texto
        self.chat_box.config(state='normal')
        self.chat_box.tag_config(color, foreground=color, font=('Arial', 14, 'bold'))
        self.chat_box.insert(tk.END, f'{user}: {msg}\n', (color,))
        self.chat_box.config(state='disabled')

    def receive_messages(self):
        # Recebe todas as mensagens que estiverem no servidor
        for response in self.stub.ReceiveMessages(chat_pb2.ReceiveRequest(username=self.username)):
            self.update_messages(response.username, response.message)
    
    def run(self):
        self.window.mainloop()

if __name__ == '__main__':
    client = ChatClient()
    client.run()

