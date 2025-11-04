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
- Servidor: o código já escuta em todas as interfaces (`0.0.0.0:5000`). Basta iniciar o servidor na máquina host.
- Cliente(s): altere o IP em `client.py` para o IP da máquina do servidor:
```python
cliente.connect(("IP_DO_SERVIDOR", 5000))
```

Como descobrir o IP do servidor:
- Linux (Terminal):
  ```bash
  hostname -I
  # ou
  ip addr show | grep -Eo 'inet (\d+\.){3}\d+' | awk '{print $2}'
  ```
- Windows:
  - Prompt de Comando: `ipconfig` (use o IPv4 da interface conectada)
  - PowerShell (opcional):
    ```powershell
    (Get-NetIPConfiguration | Where-Object {$_.IPv4Address}).IPv4Address.IPAddress
    ```
- macOS (Terminal):
  ```bash
  ipconfig getifaddr en0   # Wi‑Fi costuma ser en0; se vazio, tente en1
  # ou
  ifconfig | grep -Eo 'inet (\d+\.){3}\d+' | awk '{print $2}'
  ```

Firewall (se necessário):
- Linux (UFW):
  ```bash
  sudo ufw allow 5000/tcp
  ```
- Windows Defender Firewall:
  - GUI: crie uma regra de entrada TCP porta 5000 permitida.
  - PowerShell:
    ```powershell
    New-NetFirewallRule -DisplayName "Chat TCP 5000" -Direction Inbound -Protocol TCP -LocalPort 5000 -Action Allow
    ```
- macOS: permita conexões de entrada para o Python quando o sistema solicitar (local do Firewall varia por versão do macOS).

Observação: servidor e clientes devem estar na mesma rede/sub-rede (ex.: 192.168.x.x ou 10.x.x.x). Redes de convidados podem bloquear conexões locais.

## Como funciona (resumo)
### Servidor (`server.py`)
- Cria um socket TCP/IPv4: `socket(AF_INET, SOCK_STREAM)`.
- Faz `bind((ip, porta))` e `listen()`; na thread principal, chama `accept()` em loop.
- Mantém uma lista global `clientes` e um mapa `nomes` (socket → nome).
- Para cada novo cliente, cria uma thread (`handle_cliente`) que:
 Você verá: `Servidor iniciado.`
  - Em seguida, lê mensagens de texto com `recv(1024)`; se receber `b''` (vazio), o cliente fechou a conexão → encerra e remove.
  - Para cada texto recebido, prefixa "<nome>: ..." e chama `broadcast` para enviar aos demais clientes.

### Cliente (`client.py`)
- Conecta ao servidor com `connect((ip, porta))`.
- Lê a primeira mensagem do servidor e pede o nome ao usuário.
- Envia apenas o nome como primeira mensagem; o servidor anuncia a entrada e passará a prefixar o nome nas mensagens subsequentes.
- Cria uma thread para receber mensagens (fica em `recv()` e imprime).
- Na thread principal, lê do teclado (`input()`) e envia apenas o texto; o servidor prefixa "<nome>: ...".

## Conceitos importantes
- `AF_INET`: Address Family IPv4 (endereços como `( "127.0.0.1", 5000 )`).
- `SOCK_STREAM`: socket do tipo stream → TCP (confiável, orientado à conexão, ordenado).
- `bind()`: associa o socket a um IP/porta local (reserva esse par para o processo).
- `recv(n)`: lê até `n` bytes (retorna `bytes`). Se a outra ponta fechou a conexão, retorna `b''`.
- TCP é um fluxo: um `send` pode chegar em vários `recv` e vice‑versa; neste exemplo simples, mensagens > 1024 bytes podem ser fragmentadas.
- Threads: o cliente usa duas (envio na principal; recepção em uma thread). O servidor tem uma thread principal (accept) e uma thread por cliente (recepção e broadcast).

## Limitações atuais
- Não há protocolo de mensagens (delimitador ou tamanho). Mensagens > 1024 bytes podem ser quebradas.
 Como descobrir o IP do servidor (Linux):
 ```bash
 hostname -I
 # ou
 ip addr show | grep -Eo 'inet (\d+\.){3}\d+' | awk '{print $2}'
 ```
 Use o IP da interface conectada ao Wi‑Fi/rede local (geralmente 192.168.x.x ou 10.x.x.x).

 Se necessário, libere a porta no firewall:
 ```bash
 sudo ufw allow 5000/tcp
 ```
- A lista `clientes` é modificada por múltiplas threads sem locks (ok para demo, arriscado em produção).
- O servidor não valida nomes duplicados nem autentica usuários.
- `except:` genérico esconde erros específicos.

## Melhorias sugeridas
- Definir protocolo por linhas (terminar mensagens com `\n`) ou prefixo de tamanho.
- Proteger `clientes` com `threading.Lock()` e evitar remover enquanto itera.
- Capturar exceções específicas (`ConnectionResetError`, `BrokenPipeError`, `socket.timeout`) e adicionar logs.
- Tornar IP/porta configuráveis por argumentos de linha de comando ou variáveis de ambiente.

## Exemplo de sessão
- Terminal A (servidor): `python3 server.py`
- Terminal B (cliente 1): `python3 client.py` → nome: Ana → digita: "Oi"
- Terminal C (cliente 2): `python3 client.py` → nome: Bruno → vê: `Ana: Oi`