from saida.marcador import SILENCIAR

DEFAULT_QT_JOGOS = 300
MAX_RODADAS = 1000


def executa_simulacoes(classe_jogo, qt_jogos=None):
    """
    Executa as simulações do jogo conforme parametros
    ...
    :classe_jogo = Qual objeto-jogo deve ser
            instanciado em cada simulação
    :qt_jogos = Somente para o modo não-silencioso
            (Se SILENCIAR for True,
            usa a quantidade default)
    """
    if not qt_jogos or SILENCIAR:
        qt_jogos = DEFAULT_QT_JOGOS
    if SILENCIAR:
        limite_rodadas = MAX_RODADAS
    else:
        limite_rodadas = 50 #-- p/ não gerar muitos prints
    partidas = {}
    vitorias = {}
    soma_turnos = 0
    for i in range(qt_jogos):
        jogo = classe_jogo(i+1, limite_rodadas)
        vencedor = None
        while not vencedor:
            vencedor = jogo.atualiza()
            soma_turnos += 1
        partidas[jogo.motivo] = partidas.get(jogo.motivo, 0) + 1
        tipo_jogador = vencedor.comportamento.__class__.__name__
        vitorias[tipo_jogador] = vitorias.get(tipo_jogador, 0) + 1
    media_turnos = soma_turnos / qt_jogos
    print('='*50)
    print('::::::::: RESUMO E ESTATISTICAS :::::::::')
    print('-'*50)
    print('\tTotal de partidas = {}'.format(qt_jogos))
    print(
        '\tPartidas que terminaram em Time Out = ',
        partidas.get('TimeOut', 0)
    )
    print('\tMedia de turnos = {:.2f}'.format(media_turnos))
    print('\tVitorias por tipo:')
    melhor = None
    for tipo in vitorias:
        porcentagem = vitorias[tipo] / qt_jogos * 100
        if not melhor or porcentagem > vitorias[melhor]:
            melhor = tipo
        print('\t\t {} = {:.2f} %'.format(
            tipo,
            porcentagem
        ))
        vitorias[tipo] = porcentagem
    print('\tTipo que mais venceu = ', melhor)
    print('-'*50)
