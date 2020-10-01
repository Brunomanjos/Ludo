A aplicação é composta pelos módulos: Main, Match, Board, Player, Piece, Dice, GUI e Database.

# Main
Apenas inicia o jogo com interface visual.

# Match
Representa uma partida de ludo com as regras do jogo.

**Funcionalidades:**
* Criar nova partida, com quatro jogadores de nomes distintos.
* Carregar partida salva.
* Terminar partida, gerandom um dicionário com os dados para serem salvos.
* Selecionar o jogador do turno atual.
* Pegar a cor das peças de um jogador.
* Descobrir as jogadas possíveis para um determinado jogador.
* Fazer uma jogada: mover uma peça ou pular a vez, caso não haja opção de mover as peças.
* Verificar se a partida acabou. (três jogadores com todas as peças na região central)
* Pegar a lista dos ganhadores, ordenados do primeiro para o último colocados.


# Board
Representa o tabuleiro do jogo, com as posições válidas das peças.

**Funcionalidades:**
* Pegar as posições de origem das peças de cada cor.
* Pegar o caminho que uma peça deve fazer para se mover para outra casa. (lista das casas)

# Player
Contém os nomes dos quatro jogadores da partida.

**Funcionalidades:**
* Definir o nome dos quatro jogadores. Os nomes só podem ser definidos antes de começar a partida.
* Pegar o nome dos quatro jogadores.

# Piece
Representa as dezesseis peças coloridas.

**Funcionalidades:**
* Pegar todas as peças.
* Pegar as peças com uma determinada cor.
* Pegar a cor de uma peça.

# Dice
Simula um dado de seis lados.

**Funcionalidades:**
* Jogar dado: retorna um número entre 1 e 6, inclusive.

# GUI
Interface gráfica de interaçao com o usuário.

**Funcionalidades:**
* Abrir menu principal.
* Abrir tela de escrita do nome dos jogadores.
* Abrir tela de carregamento de um jogo salvo em banco de dados.
* Abrir tela da partida.
* Abrir menu de pause: o menu só será aberto se a tela atual for a tela da partida.
* Fechar menu de pause.
* Abrir tela dos vencedores: a tela só será aberta se a partida estiver finalizada.

# Database
Faz conexão com um banco de dados para salvar as informações das partidas.

**Funcionalidades:**
* Salvar partida.
* Baixar as últimas *n* partidas.
