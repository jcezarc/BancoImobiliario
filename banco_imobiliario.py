import random

LIMITE_RODADAS = 1000
CASAS_TABULEIRO = 20

class ItemJogo:
    @classmethod
    def get_elementos(cls, iteracoes):
        if isinstance(iteracoes, list):
            random.shuffle(iteracoes)
        lista = []
        for item in iteracoes:
            elemento = cls(item)
            lista.append(elemento)
        return lista

class Propriedade(ItemJogo):
    """
    Uma propriedade é um imóvel ocupando
    uma posição (ou `casa`) no tabuleiro
    :numero é como se fosse a numeração da rua 
            (para debug/logging...)
    :custo_venda recebe um valor qualquer, apenas como exemplo
    :valor_aluguel  recebe um valor parecido, só que menor..
    """
    def __init__(self, numero):
        self.numero = numero
        self.custo_venda = random.randrange(100, 200)
        self.valor_aluguel = random.randrange(30, 90)
        self.dono = None
    def cobra_aluguel(self, jogador):
        jogador.saldo -= self.valor_aluguel
        self.dono.saldo += self.valor_aluguel

class Jogador(ItemJogo):
    def __init__(self, comportamento):
        self.comportamento = comportamento()
        self.saldo = 300
        self.posicao = 0
    def decide_compra(self, propriedade):
        deve_comprar = self.comportamento.deve_comprar(
            propriedade,
            self
        )
        if deve_comprar:
            self.saldo -= propriedade.custo_venda
            propriedade.dono = self
    def movimenta(self, distancia, jogo):
        """
        Aqui `casa` também é uma Propriedade,
        mas é tratada como um espaço no tabuleiro
        """
        idx = self.posicao + distancia
        if idx > CASAS_TABULEIRO:
            self.saldo += 100 #--- Completou uma volta!
        idx %= CASAS_TABULEIRO
        casa = jogo.tabuleiro[idx]
        if casa.dono:
            if casa.dono == self:
                return
            casa.cobra_aluguel(self)
            if self.saldo < 0:
                jogo.remove_jogador(self)
        elif self.saldo >= casa.custo_venda:
            self.decide_compra(casa)
        self.posicao = idx

#-------- Comportamentos ------------------
class Impulsivo:
    def deve_comprar(self, propriedade, jogador):
        return True

class Exigente:
    def deve_comprar(self, propriedade, jogador):
        return propriedade.valor_aluguel > 50

class Cauteloso:
    def deve_comprar(self, propriedade, jogador):
        reserva = jogador.saldo - propriedade.custo_venda
        return reserva >= 80

class Aleatorio:
    def deve_comprar(self, propriedade, jogador):
        return bool(random.getrandbits(1))
#--------------------------------------------

class Jogo:
    def __init__(self):
        """
        Cria o tabuleiro e
        Também cria 4 jogadores:
        Um impulsivo, um exigente, um cauteloso
        e um de comportamento aleatório
        """
        self.rodadas = 0
        self.motivo = ''
        self.tabuleiro = Propriedade.get_elementos(
            range(CASAS_TABULEIRO)
        )
        self.jogadores_ativos = Jogador.get_elementos([
            Impulsivo,
            Exigente,
            Cauteloso,
            Aleatorio
        ])
        self.idx_jogador = 0 #-- Jogador atual
    def proximo_turno(self):
        if not self.jogadores_ativos:
            raise Exception('Nenhum jogador ativo')
        elif len(self.jogadores_ativos) == 1:
            return self.encerra_jogo('WO')
            #      ^^^---- vitória por W.O.
        idx = self.idx_jogador
        jogador = self.jogadores_ativos[idx]
        jogador.movimenta(random.randint(1, 6), self)
        idx += 1
        if idx >= len(self.jogadores_ativos):
            self.rodadas += 1
            if self.rodadas >= LIMITE_RODADAS:
                return self.encerra_jogo('TimeOut')
            idx = 0
        self.idx_jogador = idx
        return None
    def remove_jogador(self, perdedor):
        self.jogadores_ativos.remove(perdedor)
        for casa in self.tabuleiro:
            if casa.dono == perdedor:
                casa.dono = None
    def encerra_jogo(self, motivo):
        """
        `jogadores_ativos` está em ordem de turno
        portanto o primeiro a ser aclamado vencedor
        tem precedência sobre outro com saldo empatado.
        """
        vencedor = None
        for jogador in self.jogadores_ativos:
            if not vencedor or jogador.saldo > vencedor.saldo:
                vencedor = jogador
        self.motivo = motivo
        return vencedor

def executa_simulacoes(qt_jogos=300):
    partidas = {}
    vitorias = {}
    soma_turnos = 0
    for i in range(qt_jogos):
        jogo = Jogo()
        vencedor = None
        while not vencedor:
            vencedor = jogo.proximo_turno()
            soma_turnos += 1
        partidas[jogo.motivo] = partidas.get(jogo.motivo, 0) + 1
        tipo_jogador = vencedor.comportamento.__class__.__name__
        vitorias[tipo_jogador] = vitorias.get(tipo_jogador, 0) + 1
    media_turnos = soma_turnos / qt_jogos
    print('='*50)
    print('SIMULAÇÃO DE BANCO IMOBILIÁRIO')
    print('-'*50)
    print(
        '\tPartidas que terminaram em Time Out = ',
        partidas.get('TimeOut', 0)
    )
    print('\tMédia de turnos = {:.2f}'.format(media_turnos))
    print('\tVitorias por tipo:')
    melhor = None
    for tipo in vitorias:
        porcentagem = vitorias[tipo] / qt_jogos * 100
        if not melhor or porcentagem > vitorias[melhor]:
            melhor = tipo
        print('\t\t {} = {:.2f}%'.format(
            tipo,
            porcentagem
        ))
        vitorias[tipo] = porcentagem
    print('\tTipo que mais venceu = ', melhor)
    print('-'*50)

executa_simulacoes(300)
