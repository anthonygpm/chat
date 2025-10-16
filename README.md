# Chat TCP em Python

Um chat simples de terminal usando sockets TCP e threads. O servidor aceita múltiplas conexões e retransmite (broadcast) cada mensagem recebida para os demais clientes. O cliente conecta, informa um nome e envia mensagens pelo teclado enquanto recebe mensagens em paralelo.

## Estrutura do projeto
- `server.py` — Servidor TCP: aceita conexões, cria uma thread por cliente e faz broadcast das mensagens.
- `client.py` — Cliente TCP: conecta ao servidor, envia mensagens digitadas e imprime as recebidas.

## Requisitos
- Python 3.8+ (sem dependências externas)

## Como executar
1. Inicie o servidor (em um terminal):
```bash
python3 server.py
```
Você verá: `Servidor iniciado em 127.0.0.1:5000`

2. Em outro(s) terminal(is), inicie um ou mais clientes:
```bash
python3 client.py
```
- O cliente mostrará a mensagem de boas‑vindas do servidor.
- Digite seu nome quando solicitado e, depois, envie mensagens.

3. Cada mensagem enviada por um cliente é enviada a todos os demais clientes conectados. O remetente não recebe eco da própria mensagem pelo servidor.

### Executando em rede local (LAN)
- Servidor: altere o bind em `server.py` para escutar em todas as interfaces:
```python
servidor.bind(("0.0.0.0", 5000))
```
- Cliente(s): altere o IP em `client.py` para o IP da máquina do servidor:
```python
cliente.connect(("IP_DO_SERVIDOR", 5000))
```

## Como funciona (resumo)
### Servidor (`server.py`)
- Cria um socket TCP/IPv4: `socket(AF_INET, SOCK_STREAM)`.
- Faz `bind((ip, porta))` e `listen()`; na thread principal, chama `accept()` em loop.
- Mantém uma lista global `clientes` com os sockets conectados.
- Para cada novo cliente, cria uma thread (`handle_cliente`) que:
  - Lê do socket com `recv(1024)`.
  - Se receber `b''` (vazio), o cliente fechou a conexão → encerra a thread e remove da lista.
  - Caso contrário, chama `broadcast(mensagem, cliente)` para enviar a todos os outros.

### Cliente (`client.py`)
- Conecta ao servidor com `connect((ip, porta))`.
- Lê a primeira mensagem do servidor e pede o nome ao usuário.
- Cria uma thread para receber mensagens (fica em `recv()` e imprime).
- Na thread principal, lê do teclado (`input()`) e envia com `send()`.

## Conceitos importantes
- `AF_INET`: Address Family IPv4 (endereços como `( "127.0.0.1", 5000 )`).
- `SOCK_STREAM`: socket do tipo stream → TCP (confiável, orientado à conexão, ordenado).
- `bind()`: associa o socket a um IP/porta local (reserva esse par para o processo).
- `recv(n)`: lê até `n` bytes (retorna `bytes`). Se a outra ponta fechou a conexão, retorna `b''`.
- TCP é um fluxo: um `send` pode chegar em vários `recv` e vice‑versa; neste exemplo simples, mensagens > 1024 bytes podem ser fragmentadas.
- Threads: o cliente usa duas (envio na principal; recepção em uma thread). O servidor tem uma thread principal (accept) e uma thread por cliente (recepção e broadcast).

## Limitações atuais
- Não há protocolo de mensagens (delimitador ou tamanho). Mensagens > 1024 bytes podem ser quebradas.
- O servidor não armazena nomes; o cliente prefixa o nome no texto enviado.
- A lista `clientes` é modificada por múltiplas threads sem locks (ok para demo, arriscado em produção).

## Melhorias sugeridas
- Definir protocolo por linhas (terminar mensagens com `\n`) ou prefixo de tamanho.
- Proteger `clientes` com `threading.Lock()` e evitar remover enquanto itera.
- Capturar exceções específicas (`ConnectionResetError`, `BrokenPipeError`, `socket.timeout`) e adicionar logs.
- Tornar IP/porta configuráveis por argumentos de linha de comando ou variáveis de ambiente.

## Exemplo de sessão
- Terminal A (servidor): `python3 server.py`
- Terminal B (cliente 1): `python3 client.py` → nome: Ana → digita: "Oi"
- Terminal C (cliente 2): `python3 client.py` → nome: Bruno → vê: `Ana: Oi`