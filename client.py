from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

def receber_mensagens(sock):
    while True:
        try:
            msg = sock.recv(1024).decode('utf-8')
            if not msg:
                break
            print(msg)
        except:
            break

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(('localhost', 12345))

nome = input("Qual seu nome para se registrar no servidor? ")
client_socket.send(nome.encode('utf-8'))

Thread(target=receber_mensagens, args=(client_socket,), daemon=True).start()

while True:
    try:
        msg = input()
        if msg.lower() == 'sair':
            break
        client_socket.send(msg.encode('utf-8'))
    except:
        break

client_socket.close()
