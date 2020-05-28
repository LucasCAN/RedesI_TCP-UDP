import sys
import json
import socket
import struct
from math import radians, cos, sin, asin, sqrt

def get_address():
    #retorna endereço da maquina para conexão
    try:
        addr = socket.gethostbyname(socket.gethostname())
    except:
        addr = None
    finally:
        if not addr or addr.startswith("127."):
            host = "1.1.1.1"
            port = 80
            
            conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            conn.connect((host, port))

            addr = conn.getsockname()[0]
            conn.close()

        return addr

def isInside(coord, center, radius):

    lat = coord[0]
    lon = coord[1]
    x = center[0]
    y = center[1]

    # Compara o raio com a distancia do centro com a coordenada  
    if ((x - lat) * (x - lat) + 
        (y - lon) * (y - lon) <= radius * radius): 
        return True; 
    else: 
        return False; 

def prepara_serverUdp(server_udp, arquivo):
    msg, client = server_udp.recvfrom(1024)
    json_message = json.loads(msg.decode())

    server_udp.sendto(str(json_message['id']).encode(), client)

    print('Mensagem {} recebida'.format(str(json_message['id'])))

    if json_message['tipo'] == 'D':

        json.dump({
            'combustivel': json_message['combustivel'], 
            'preco': json_message['preco'], 
            'coordenada': json_message['coordenada']
        }, arquivo)
        arquivo.write('\n')
        arquivo.flush()
    
    else:
        arquivo.seek(0)
        dados = arquivo.readlines() #json.load(arquivo)
        
        menor = sys.maxsize

        for i in range(len(dados)):
            s = json.loads(dados[i])
            
            if isInside(s['coordenada'], json_message['centro'], json_message['raio']) \
            and s['combustivel'] == json_message['combustivel'] \
            and s['preco'] < menor:
                menor = s ['preco']

        server_udp.sendto(str(menor).encode(), client)



def start_server():
    #inicializa servidor
    host = get_address()
    port = int(input('Insira a porta para conexão: '))

    # Cria o socket através do parâmetro AF_INET
    # e usa o protocolo UDP pelo SOCKET_DGRAM.
    server_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_udp.bind((host, port))

    print('Servidor iniciado. Aguardando conexões...')
    print('Host: {}\nPorta: {}'.format(host, port))

    arquivo = open('precos.json','a+') 


    # Inicia a escuta por possíveis conexões
    _, client = server_udp.recvfrom(1024)
    print('{} conectado. Preparando...'.format(client[0]))

    while True:
        prepara_serverUdp(server_udp, arquivo)

    arquivo.close()
    server_udp.close()

if __name__ == '__main__':
    start_server()