import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, Entry, Button, simpledialog

class ChatClient:
    def __init__(self):
        # Obter o IP do servidor e o nome de usuário
        self.host = simpledialog.askstring('Conexão ao Servidor', 'Digite o IP do servidor:\n(Deixar em branco = localhost)')

        if self.host == '' or self.host == '172.0.0.1':
            self.host = 'localhost'

        while True:
            self.username = simpledialog.askstring('Conexão ao Servidor', 'Digite seu nome de usuário:\n (No mínimo 3 letras)')

            if len(self.username) >= 3:
                break

        # Conexão com o servidor usando sockets
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((self.host, 8888))
            self.client_socket.send(self.username.encode('utf-8'))
        except ConnectionRefusedError:
            print("Não foi possível conectar ao servidor.")
            exit()

        # Cria a tela principal
        self.window = tk.Tk()
        self.window.title(f'Chat de {self.username} - Conectado em {self.host}')

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

        # Thread para receber as mensagens do servidor socket
        threading.Thread(target=self.receive_messages).start()

    def send_message(self):
        # Pega a mensagem da caixa de entrada fazendo TRIM
        message = self.message_entry.get().strip()
        
        # Se não vazia concatena a mensagem com o nome do usuário e manda para o servidor
        if len(message):
            full_message = f'{self.username}: {message}'
            self.client_socket.send(full_message.encode('utf-8'))
        
        # Limpa e focaliza o campo de entrada
        self.message_entry.delete(0, tk.END)
        self.message_entry.focus()

    def update_messages(self, message):
        # Cor azul para mensagen de outros usuário, vermelho para prórpia
        color = '#0000FF'
        if message.split(':')[0] == self.username:
            color = '#FF0000'

        # Escreve a mensagem na caixa de texto
        self.chat_box.config(state='normal')
        self.chat_box.tag_config(color, foreground=color, font=('Arial', 14, 'bold'))
        self.chat_box.insert(tk.END, message + '\n', (color,))
        self.chat_box.config(state='disabled')

    def receive_messages(self):
        while True:
            try:
                # Recebe a mensagem do servidor e manda escrever na caixa de texto
                message = self.client_socket.recv(1024).decode('utf-8')
                self.update_messages(message)
            except:
                # Em caso de erro sair
                print('Erro ao receber mensagem')
                self.client_socket.close()
                break

    def run(self):
        self.window.mainloop()

if __name__ == '__main__':
    client = ChatClient()
    client.run()

