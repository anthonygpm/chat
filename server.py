import socket
import threading

# Lista para guardar os clientes conectados
clientes = []

# Função que envia uma mensagem para todos os clientes conectados
def broadcast(mensagem, cliente_atual):
    for cliente in clientes:
        if cliente != cliente_atual:
            try:
                cliente.send(mensagem)
            except:
                cliente.close()
                clientes.remove(cliente)

# Função que trata as mensagens de um cliente
def handle_cliente(cliente):
    while True:
        try:
            mensagem = cliente.recv(1024)
            if not mensagem:
                break
            broadcast(mensagem, cliente)
        except:
            cliente.close()
            if cliente in clientes:
                clientes.remove(cliente)
            break

# Configura o servidor
def iniciar_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(("127.0.0.1", 5000))  # IP local e porta
    servidor.listen()
    print("Servidor iniciado em 127.0.0.1:5000")

    while True:
        cliente, endereco = servidor.accept()
        print(f"Conectado a {endereco}")
        clientes.append(cliente)
        cliente.send("Bem-vindo ao chat! Digite seu nome:".encode("utf-8"))
        thread = threading.Thread(target=handle_cliente, args=(cliente,))
        thread.start()

if __name__ == "__main__":
    iniciar_servidor()
