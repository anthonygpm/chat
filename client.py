import socket 
import threading

# Função para receber mensagens do servidor
def receber_mensagens(cliente):
    while True:
        try:
            mensagem = cliente.recv(1024).decode("utf-8") # decodifica bytes para string
            print(mensagem) # exibe a mensagem recebida
        except:
            print("Conexão encerrada pelo servidor.")
            cliente.close()
            break

# Função para enviar mensagens ao servidor
def enviar_mensagens(cliente, nome):
    while True:
        mensagem = input()
        cliente.send(mensagem.encode("utf-8")) # codifica string para bytes e envia; servidor prefixa o nome

# Conecta ao servidor
def iniciar_cliente():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Cria um socket IPV4 e TCP
    cliente.connect(("127.0.0.1", 5000)) # Conecta ao servidor no IP e porta especificados

    # Primeira mensagem de boas-vindas do servidor
    print(cliente.recv(1024).decode("utf-8")) # decodifica bytes para string e exibe
    nome = input("Digite seu nome:")
    cliente.send(nome.encode("utf-8")) # envia apenas o nome; o servidor anuncia "entrou"

    # Thread para receber mensagens
    thread_receber = threading.Thread(target=receber_mensagens, args=(cliente,)) # Cria uma thread para receber mensagens
    thread_receber.start() # Inicia a thread

    # Envia mensagens na thread principal
    enviar_mensagens(cliente, nome)

if __name__ == "__main__":
    iniciar_cliente()
