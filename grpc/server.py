import grpc
from concurrent import futures
import chat_pb2
import chat_pb2_grpc

class ChatServiceServicer(chat_pb2_grpc.ChatServiceServicer):
    def __init__(self):
        # Cria a lista para armazenar as 10 primeiras mensagens
        self.messages = []

    def SendMessage(self, request, context):
        # Copia a mensagem e o nome de usuário
        message = request.message
        username = request.username

        # Limita às útimas 10 mensagens salvas
        if len(self.messages) == 10:
            self.messages.pop()

        # Adiciona a nova mensagem
        self.messages.append((username, message))

        return chat_pb2.MessageResponse(username=username, message=message)

    def ReceiveMessages(self, request, context):
        last_index = 0
        while True:
            # Loop nas mensagens salvas
            while len(self.messages) > last_index:
                # Copia o nome de usuário e mensagem na tupla de mensagens
                username = self.messages[last_index][0]
                message = self.messages[last_index][1]
                
                last_index += 1
                
                yield chat_pb2.MessageResponse(username=username, message=message)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print('Servidor iniciado na porta 50051...')
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

