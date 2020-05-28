import json
import socket
import struct
import enum

Turn = enum.Enum('Turn', 'ENEMY PLAYER')
MoveStatus = enum.Enum('MoveStatus', 'HIT MISS INVALID')
MoveResult = {
    MoveStatus.HIT: 'Acerto',
    MoveStatus.MISS: 'Erro',
    MoveStatus.INVALID: 'Movimento Inválido',
}

Winner = enum.Enum('Winner', 'NONE SERVER PLAYER')

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


def mostra_jogo(navios, num_navios, boards, hits):
    """ Mostra na tela o estado atual do jogo. 
    
    @param navios tipos de navios.
    @param num_navios quantidade de navios.
    @param boards tabuleiros (inimigo e jogador).
    @param hits acertos (inimigo e jogador).
    """
    
    column = 'A'

    print('\nTabuleiro Server\t\t\t\t\tMeu Tabuleiro')

    # Imprime os tabuleiros do inimigo e do jogador
    enemy_rows = '  ' + ' | '.join([str(i) for i in range(1, num_navios + 1)])
    player_rows = '  ' + '  | '.join([str(i) for i in range(1, num_navios + 1)])
    print('  {}\t\t  {}'.format(enemy_rows, player_rows))

    
    for enemy_row, player_row in zip(boards['enemy'], boards['player']):
        player_row = list(map(
            lambda x: '- ' if x == '-' else x,
            player_row
        ))

        print(column + ' | '  + ' | '.join(enemy_row) +  ' | ' + '\t\t' + column + ' | '  + ' | '.join(player_row)+  ' | ' )
        column = chr(ord(column) + 1)

    # Imprime a quantidade de navios afundados
    print('O inimigo acertou {} posições'.format(hits['enemy']))
    print('Você acertou {} posições\n'.format(hits['player']))

    print('Legenda:')
    for _, ship in navios.items():
        print('{}: {}'.format(ship['symbol'], ship['name']))
    print('*: Falha')
    print('x: Acerto')
    print('-: Posição livre\n')


def print_meuGame(navios, num_navios, boards, hits):
    """ Mostra na tela o estado atual do jogo. 
    
    @param navios tipos de navios.
    @param num_navios quantidade de navios.
    @param boards tabuleiros (inimigo e jogador).
    @param hits acertos (inimigo e jogador).
    """
    
    column = 'A'

    print('\nMeu Tabuleiro')

    # Imprime os tabuleiros do inimigo e do jogador
    player_rows = '  ' + '  | '.join([str(i) for i in range(1, num_navios + 1)])
    print('  {}\t\t  {}'.format(enemy_rows, player_rows))

    
    for player_row in zip(boards['player']):
        player_row = list(map(
            lambda x: '- ' if x == '-' else x,
            player_row
        ))

        print(column + ' | '  + ' | '.join(player_row)+  ' | ' )
        column = chr(ord(column) + 1)

    print('Legenda:')
    for _, ship in navios.items():
        print('{}: {}'.format(ship['symbol'], ship['name']))
    print('*: Falha')
    print('x: Acerto')
    print('-: Posição livre\n')


def get_row(board_size):
    """ Retorna uma linha válida do tabuleiro, de acordo
    com a posição informada pelo jogador. 
    @param board_size tamanho do tabuleiro.
    @return inteiro representando a linha.
    """
    
    row = 'A'
    valid_pos = False
    while not valid_pos:
        try:
            row = (input('Escolha uma linha (A-J): '))
            row = row.upper()

            if ord(row) < ord('A') or ord(row) >= ord('A') + board_size:
                raise Exception()

            valid_pos = True
        except Exception:
            print('Caractere Inválido')

    return ord(row) - ord('A')


def get_column(board_size):
    """ Retorna uma coluna válida do tabuleiro, de acordo
    com a posição informada pelo jogador. 
    
    @param board_size tamanho do tabuleiro.
    @param inteiro representando a coluna.
    """
    
    col = 0
    valid_pos = False
    while not valid_pos:
        try:
            col = int(input('Escolha uma coluna (1-10): '))

            if col < 1 or col >= 1 + board_size:
                raise Exception()
            
            valid_pos = True
        except ValueError:
            print('Valor Inválido.')
        except Exception:
            print('Valor fora do Limite.')

    return col - 1
    

def get_direction():
    """ Retorna a orientação em que será colocado o navio (horizontal
    ou vertical).
    @return inteiro representando a direção, sendo 1 para horizontal e
    0 para vertical.
    """
    
    valid_dir = False
    while not valid_dir:
        try:
            d = input('Insira a direção (Horizontal: H, Vertical: V): ')
            d = d.upper()

            if d not in ['H', 'V']:
                raise Exception()

            valid_dir = True
        except Exception:
            print('Direção inválida!')
            
    return 1 if d == 'H' else 0


def get_coord(board_size):
    """ Retorna a coordenada informada pelo jogador. 
    @param board_size tamanho do tabuleiro.
    @return tupla contendo dois elementos: linha e coluna.
    """
    
    i = get_row(board_size)
    j = get_column(board_size)

    return (i, j)


def place_ship(board, board_size, ship, ship_number):
    """ Posiciona navio no tabuleiro, de acordo
    com posição informada pelo jogador. 
    @param board tabuleiro.
    @param ship tipo de navio.
    """

    fit = False
    positions = []
    
    while not fit:
        row, col = get_coord(board_size)
        direction = get_direction()
        
        for s in range(ship['size']):
            r = row + s * (1 - direction)
            c = col + s * direction

            if (r >= len(board) or c >= len(board[0]) or
                board[r][c] != '-'):
                
                break
            elif s == ship['size'] - 1:
                fit = True
                positions = [(row + (1 - direction) * i,
                              col + direction * i)
                             for i in range(ship['size'])]

        if not fit:
            print('Posição inválida!')

    for i, j in positions:
        board[i][j] = ship['symbol'] + str(ship_number)
        
    
def new_board(navios, num_navios, board_size):
    """ Cria um novo tabuleiro, de acordo com as escolhas
    do jogador.
    @param navios tipos de navios.
    @param num_navios quantidade de navios.
    @param board_size tamanho do tabuleiro.
    
    @return matriz representando o tabuleiro.
    """

    enemy_board = [['-' for _ in range(board_size)]
                   for _ in range(board_size)]
    player_board = [['-' for _ in range(board_size)]
                    for _ in range(board_size)]

    for key, ship in navios.items():
        # Posiciona navio de acordo com tipo.
        for i in range(ship['quantity']):
            place_ship(player_board, board_size, navios[key], (i + 1))
            mostra_jogo(
                navios, num_navios,
                {'player': player_board, 'enemy': enemy_board},
                {'player': 0, 'enemy': 0}
            )
    
    return player_board


#inicializa client tcp com jogo batalha naval
def prepara_client():
     
    print(' ')
    print('{} Batalha Naval {}\n'.format(' ' * 29, ' ' * 28))
    host = input('Insira o IP do servidor: ')
    port = int(input('Insira a porta para conexão: '))

    # Cria o socket através do parâmetro AF_INET
    # e usa o protocolo UDP pelo SOCKET_STREAM.
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    # recebe pack com dadosdo jogo
    board_size, = struct.unpack('!I', client.recv(4))
    num_navios, = struct.unpack('!I', client.recv(4))
    
    length, = struct.unpack('!I', client.recv(4))
    navios = json.loads(client.recv(length).decode())

    # Tabuleiro do lado do server
    enemy_board = [['-' for _ in range(board_size)]
                   for _ in range(board_size)]

    # Tabuleiro do jogador/ do client
    player_board = new_board(navios, num_navios, board_size)

    # informaçoes dos tabuleiros 
    boards = {'player': player_board, 'enemy': enemy_board}

    # manda tabuleiros para o server
    data = json.dumps(boards['player']).encode()
    client.send(struct.pack('!I', len(data)))
    client.send(data)
    
    print('\n\nJogo começou!')
    init_game(client, navios, num_navios, boards, board_size)


def init_game(conn, navios, num_navios, boards, board_size):
    # Jogador - client - começa o 1 turno
    turn = Turn.PLAYER
    winner = Winner.NONE
        
    while winner == Winner.NONE:
        if turn == Turn.PLAYER:
            i, j = get_coord(board_size)
            data = json.dumps({'row': i, 'col': j}).encode()
            conn.send(struct.pack('!I', len(data)))
            conn.send(data)
            data, = struct.unpack('!I', conn.recv(4))
            res = MoveStatus(data)
            print('Resultado da sua ultima jogada: {}'.format(
                MoveResult[res]
            ))

            if res == MoveStatus.HIT:
                boards['enemy'][i][j] = 'x'
            elif res == MoveStatus.MISS:
                boards['enemy'][i][j] = '*'

        else:
            length, = struct.unpack('!I', conn.recv(4))
            i, j = json.loads(conn.recv(length).decode()).values()
            
            data, = struct.unpack('!I', conn.recv(4))
            res = MoveStatus(data)

            print('Resultado da ultima jogada inimiga: {}'.format(
                MoveResult[res]
            ))
            
            if res == MoveStatus.HIT:
                boards['player'][i][j] = 'x '
            elif res == MoveStatus.MISS:
                boards['player'][i][j] = '* '

        if res != MoveStatus.INVALID:
            length, = struct.unpack('!I', conn.recv(4))
            hits = json.loads(conn.recv(length).decode())

            input('Pressione ENTER para continuar!')
            mostra_jogo(navios, num_navios, boards, hits)

            data, = struct.unpack('!I', conn.recv(4))
            turn = Turn(data)
            
            data, = struct.unpack('!I', conn.recv(4))
            winner = Winner(data)

    if winner == Winner.PLAYER:
        print('Você venceu!')
    else:
        print('Você perdeu!')
        
if __name__ == '__main__':
    prepara_client()