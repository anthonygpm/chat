import socket
import threading

# Função para receber mensagens do servidor
def receber_mensagens(cliente):
    while True:
        try:
            mensagem = cliente.recv(1024).decode("utf-8")
            print(mensagem)
        except:
            print("Conexão encerrada pelo servidor.")
            cliente.close()
            break

# Função para enviar mensagens ao servidor
def enviar_mensagens(cliente, nome):
    while True:
        mensagem = input()
        cliente.send(f"{nome}: {mensagem}".encode("utf-8"))

# Conecta ao servidor
def iniciar_cliente():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect(("127.0.0.1", 5000))

    # Primeira mensagem de boas-vindas do servidor
    print(cliente.recv(1024).decode("utf-8"))
    nome = input("Seu nome: ")
    cliente.send(nome.encode("utf-8"))

    # Thread para receber mensagens
    thread_receber = threading.Thread(target=receber_mensagens, args=(cliente,))
    thread_receber.start()

    # Thread para enviar mensagens
    enviar_mensagens(cliente, nome)

if __name__ == "__main__":
    iniciar_cliente()
