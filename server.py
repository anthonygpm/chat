import socket
import threading

# Lista para guardar os clientes (sockets) conectados
clientes = []
# Mapa de sockets para nomes de usuários
nomes = {}

# Função que envia uma mensagem para todos os clientes conectados
def broadcast(mensagem, cliente_atual):
    # Itera sobre uma cópia para evitar problemas ao remover durante a iteração
    for cliente in clientes[:]:
        if cliente != cliente_atual:  # Não envia a mensagem de volta para o remetente
            try:
                cliente.send(mensagem)
            except:
                # Remove clientes com erro
                try:
                    cliente.close()
                finally:
                    if cliente in clientes:
                        clientes.remove(cliente)
                    if cliente in nomes:
                        del nomes[cliente]

# Função que trata as mensagens de um cliente
def handle_cliente(cliente):
    nome = None
    try:
        # Primeira mensagem deve ser o nome do usuário
        nome_bytes = cliente.recv(1024)
        if not nome_bytes:
            return  # desconectou antes de enviar o nome
        nome = nome_bytes.decode("utf-8").strip()
        nomes[cliente] = nome
        # Anuncia entrada para todos (inclusive para quem entrou)
        anuncio_entrada = f"{nome} entrou no chat.".encode("utf-8")
        # Para enviar a todos, passamos cliente_atual=None
        broadcast(anuncio_entrada,None)
        # Loop principal de mensagens
        while True:
            mensagem = cliente.recv(1024)  # bytes da rede
            if not mensagem:  # cliente desconectou
                break
            texto = mensagem.decode("utf-8").strip()
            if not texto:
                continue  # ignora linhas vazias
            saida = f"{nome}: {texto}".encode("utf-8")
            broadcast(saida, cliente)
    except:
        # erros de conexão, etc.
        pass
    finally:
        # Limpeza e anúncio de saída
        try:
            cliente.close()
        finally:
            if cliente in clientes:
                clientes.remove(cliente)
            if cliente in nomes:
                nome = nomes.pop(cliente)
                try:
                    anuncio_saida = f"{nome} saiu do chat.".encode("utf-8")
                    broadcast(anuncio_saida,None)
                except:
                    pass

# Configura o servidor
def iniciar_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria um socket TCP. AF_INET (Address Family) indica IPv4 e SOCK_STREAM (Socket Type) indica TCP
    servidor.bind(("0.0.0.0", 5000))  # Associa o socket a um endereço IP e porta. Reserva o par para o processo
    servidor.listen() # Começa a escutar conexões
    print("Servidor iniciado.")

    while True:
        cliente, endereco = servidor.accept() # Aceita uma nova conexão, obtendo um novo socket para comunicação com o cliente e o endereço do cliente
        print(f"Conectado a {endereco}") # Mostra o endereço do cliente conectado
        clientes.append(cliente) # Adiciona o novo cliente à lista de clientes conectados
        cliente.send("Bem-vindo ao chat!".encode("utf-8"))
        thread = threading.Thread(target=handle_cliente, args=(cliente,)) # Cria uma nova thread para tratar as mensagens do cliente
        thread.start() # Inicia a thread

if __name__ == "__main__":
    iniciar_servidor()
