import socket
import json
import random



#Retorna tipo de entrada enviada ao servidor(dados D ou pesquisa P)
def entrada_tipo_mensagem():
	boolean = False

	while not boolean:
		try:
			entrada = input('\nQual o tipo de mensagem? (Dados = D ou Pesquisa = P): ')
			entrada = entrada.upper()

			if entrada not in ['D', 'P']:
				raise Exception()

			boolean = True
		except Exception:
			print('Tipo inválido! (Digite D ou P)')
		
	return entrada


#Retorna o tipo de combustivel ( 0-diesel, 1- álcool, 2-gasolina)
def entrada_combustivel():
	boolean = False

	while not boolean:
		try:
			entrada = int(input('\nQual o tipo de combustivel? (0-diesel, 1-álcool, 2-gasolina): '))
			#entrada = entrada.upper()

			if entrada not in [0,1,2]:
				raise Exception()

			boolean = True
		except Exception:
			print('Tipo inválido! (0-diesel, 1-álcool, 2-gasolina)')
		
	return entrada


#Retorna o preco do combustivel (inteiro x 1000)
def entrada_preco():
	boolean = False

	while not boolean:
		try:
			entrada = int(input('\nQual o preco do combustivel? '))

			boolean = True
		except Exception:
			print('Preço inválido! - (ex: 3299 = R$3,299)')
		
	return entrada

#Retorna a coordenada do posto de combustivel
def entrada_coordenada():
	boolean = False

	while not boolean:
		try:
			lat = int(input('\nQual a latitude do posto de combustivel? '))
			lon = int(input('\nQual a longitude do posto de combustivel? '))

			boolean = True
		except Exception:
			print('Coordenadada Inválida!')
		
	return lat,lon

#raio da busca/pesquisa
def entrada_raio():
	boolean = False

	while not boolean:
		try:
			raio = int(input('\nQual é o raio da busca? '))

			boolean = True
		except Exception:
			print('Raio Inválido!')
		
	return raio

#Retorna o centro(coordenadas) da busca
def entrada_centro():
	boolean = False

	while not boolean:
		try:
			lat = int(input('\nQual a latitude do centro da busca? '))
			lon = int(input('\nQual a longitude do centro da busca? '))

			boolean = True
		except Exception:
			print('Coordenadada Inválida!')
		
	return lat,lon

	#inicializa client do udp
def prepara_client():
    
    print(' ')
    print('{} Sistema de Preços {}\n'.format(' ' * 29, ' ' * 28))
    host = input('Insira o IP do servidor: ')
    port = int(input('Insira a porta para conexão: '))

    # Cria o socket através do parâmetro AF_INET
    # e usa o protocolo UDP pelo SOCKET_DGRAM.    
    client_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr = (host, port)

    client_udp.sendto(''.encode(), addr)


    id_mensagem = 0
    while True:
    	init(id_mensagem,client_udp,addr)
    	id_mensagem = id_mensagem + 1   	


    client_udp.close()


#popula arquivo com dados inseridos
def init(id_mensagem,client,addr):
	dados = ''
	tipo_entrada = entrada_tipo_mensagem()
	tipo_combustivel = entrada_combustivel()

	if tipo_entrada == 'D':
		preco = entrada_preco()
		coordenada = entrada_coordenada()

		dados = json.dumps({
			'tipo': 'D', 
			'id': id_mensagem, 
			'combustivel': tipo_combustivel, 
			'preco': preco, 
			'coordenada': coordenada
			}).encode()

		client.sendto(dados,addr)

		'''
		file = open("precos.in", "a")
		file.write('D'+"\n")
		file.write(str(id_mensagem)+"\n")
		file.write(str(tipo_combustivel)+"\n")
		file.write(str(preco)+"\n")
		file.write(str(coordenada)+"\n")
		file.write("\n")
		file.write("///")
		file.write("\n")
		file.close()
		'''

		try:
			client.settimeout(7.0)
			msg, _ = client.recvfrom(1024)
			print('Confirmado: {}'.format(msg.decode()))

		except Exception as ex:
			print('nRetransmissão...')
			client.sendto(dados, addr)


	else: #tipo_entrada == 'P':
		raio = entrada_raio()
		centro = entrada_centro()

		dados = json.dumps({
			'tipo': 'P', 
			'id': id_mensagem, 
			'combustivel': tipo_combustivel, 
			'raio': raio, 
			'centro': centro
			}).encode()

		client.sendto(dados,addr)

		try:
			client.settimeout(7.0)
			msg, _ = client.recvfrom(1024)
			if id_msg == int(msg.decode()):
				print('\nConfirmado: {}'.format(msg.decode()))
			else:
				print('\nMensagem não confirmada: {}'.format(id_msg))

		except Exception as ex:
			print('\nRetransmissão...')
			client.sendto(dados, addr)

		msg, _ = client.recvfrom(1024)
		print('\nMenor preço encontrado: {}'.format(msg.decode()))


if __name__ == '__main__':
	prepara_client()