from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

usuarios = {}  

def atender_cliente(csocket):
    nome = csocket.recv(1024).decode('utf-8')
    if nome in usuarios:
        csocket.send(f"Nome '{nome}' já está em uso.".encode('utf-8'))
        csocket.close()
        return

    usuarios[nome] = csocket
    print(f"{nome} conectado.")

    while True:
        csocket.send("Digite o nome do usuário com quem deseja conversar: ".encode('utf-8'))
        destino = csocket.recv(1024).decode('utf-8')

        if destino == nome:
            csocket.send("Você não pode conversar consigo mesmo.".encode('utf-8'))
            continue

        if destino in usuarios:
            csocket.send(f"Iniciando conversa com {destino}. Digite mensagens abaixo:\n".encode('utf-8'))
            break
        else:
            csocket.send("Usuário não encontrado. Tente outro.\n".encode('utf-8'))

    while True:
        try:
            mensagem = csocket.recv(1024).decode('utf-8')
            if not mensagem:
                break
            usuarios[destino].send(f"{nome}: {mensagem}".encode('utf-8'))
        except:
            break

    print(f"{nome} desconectado.")
    del usuarios[nome]
    csocket.close()


def main():
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen()
    print("Servidor ouvindo na porta 12345...")

    while True:
        client_socket, _ = server_socket.accept()
        Thread(target=atender_cliente, args=(client_socket,), daemon=True).start()

main()
