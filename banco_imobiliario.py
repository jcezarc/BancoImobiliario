import random

class Sequencia:
    def __init__(self):
        self.anterior = None
        self.proximo = None
    def liga_com(self, outro):
        self.proximo = outro
        outro.anterior = self
    @classmethod
    def get_sequencia(cls, iteracoes):
        primeiro = None
        ultimo = None
        lista = []
        for item in iteracoes:
            elemento = cls(item)
            if primeiro is None:
                primeiro = elemento
            if ultimo:
                ultimo.liga_com(elemento)
            ultimo = elemento
            lista.append(elemento)
        ultimo.liga_com(primeiro)
        return primeiro, lista

class Propriedade(Sequencia):
    """
    Uma propriedade é um imóvel ocupando
    uma posição (ou `casa`) no tabuleiro
    :numero é como se fosse a numeração da rua 
            (para debug/logging...)
    :valor_venda recebe um valor qualquer, apenas como exemplo
    :valor_aluguel  recebe um valor parecido, só que menor..
    """
    def __init__(self, numero):
        super().__init__()
        self.numero = numero
        self.valor_venda = random.randrange(100, 200)
        self.valor_aluguel = random.randrange(30, 60)
        self.dono = None

class Jogador(Sequencia):
    def __init__(self, comportamento):
        super().__init__()
        self.comportamento = comportamento()
        self.saldo = 300
        self.posicao = None
        self.turno = 0
    def decide_compra(self, propriedade):
        deve_comprar = self.comportamento.deve_comprar(
            propriedade,
            self
        )
        if deve_comprar:
            self.saldo -= propriedade.valor_venda
            propriedade.dono = self
    def paga_aluguel(self, propriedade):
        valor = propriedade.valor_aluguel
        self.saldo -= valor
        propriedade.dono.ganha_bonus(valor)
    def ganha_bonus(self, valor):
        self.saldo += valor
    def move(self, movimento, jogo):
        """
        Aqui `casa` também é uma Propriedade,
        mas é tratada como um espaço no tabuleiro
        ...
        Quanto ao movimento casa-por-casa,
        apesar de menos rápido, pode permitir
        futuras variações como `pedágio`
        """
        casa = self.posicao
        if casa is None:
            casa = jogo.primeira_casa
        while movimento:
            casa = casa.proximo
            movimento -=  1
        self.posicao = casa
        if casa == jogo.primeira_casa:
            self.ganha_bonus(100) #--- Completou uma volta!
        if casa.dono is None:
            if self.saldo < casa.valor_venda:
                return
            self.decide_compra(casa)
        else:
            self.paga_aluguel(casa)
            if self.saldo < 0:
                jogo.remove_jogador(self)

#-------- Comportamentos ------------------
class Impulsivo:
    def deve_comprar(self, propriedade, jogador):
        return True
    def descricao(self):
        return 'Impulsivo'

class Exigente:
    def deve_comprar(self, propriedade, jogador):
        return propriedade.valor_aluguel > 50
    def descricao(self):
        return 'Exigente'

class Cauteloso:
    def deve_comprar(self, propriedade, jogador):
        reserva = jogador.saldo - propriedade.valor_venda
        return reserva >= 80
    def descricao(self):
        return 'Cauteloso'

class Aleatorio:
    def deve_comprar(self, propriedade, jogador):
        return bool(random.getrandbits(1))
    def descricao(self):
        return 'Aleatorio'
#--------------------------------------------

class Jogo:
    def __init__(self):
        """
        Cria e posiciona na primeira `casa`
        do tabuleiro
        Também cria 4 jogadores:
        Um impulsivo, um exigente, um cauteloso
        e um de comportamento aleatório
        """
        self.rodadas = 0
        self.motivo = ''
        casa, tabuleiro = Propriedade.get_sequencia(
            range(20)
        )
        self.primeira_casa = casa
        self.tabuleiro = tabuleiro
        jogador_atual, jogadores = Jogador.get_sequencia([
            Impulsivo,
            Exigente,
            Cauteloso,
            Aleatorio
        ])
        self.jogador = jogador_atual
        self.jogadores_ativos = jogadores
    def rodada_completa(self, turno_atual):
        for jogador in self.jogadores_ativos:
            if jogador.turno != turno_atual:
                return False
        return True
    def proximo_turno(self):
        if not self.jogadores_ativos:
            raise Exception('Nenhum jogador ativo')
        elif len(self.jogadores_ativos) == 1:
            return self.encerra_jogo('Restou só 1 jogador')
        self.jogador.move(random.randint(1, 6), self)
        self.jogador.turno = self.jogador.turno + 1
        if self.rodada_completa(self.jogador.turno):
            self.rodadas += 1
            if self.rodadas > 999:
                return self.encerra_jogo('Time out')
        self.jogador = self.jogador.proximo
        return None
    def remove_jogador(self, perdedor):
        self.jogadores_ativos.remove(perdedor)
        for casa in self.tabuleiro:
            if casa.dono == perdedor:
                casa.dono = None
        perdedor.anterior.liga_com(perdedor.proximo)
    def encerra_jogo(self, motivo):
        vencedor = None
        for jogador in self.jogadores_ativos:
            if not vencedor or jogador.saldo > vencedor.saldo:
                vencedor = jogador
        self.motivo = motivo
        return vencedor

def executua_simulacoes(qt_jogos=300):
    resumo = {}
    soma_turnos = 0
    for i in range(qt_jogos):
        jogo = Jogo()
        vencedor = None
        while not vencedor:
            vencedor = jogo.proximo_turno()
        soma_turnos += vencedor.turno
        resumo[jogo.motivo] = resumo.get(jogo.motivo, 0) + 1
        tipo_jogador = vencedor.comportamento.descricao
        resumo[tipo_jogador] = resumo.get(tipo_jogador, 0) + 1
    media_turnos = soma_turnos / qt_jogos
    print('='*50)
    print('\tEstatísticas:')
    print(resumo)
    print('-'*50)
    print('Média de turnos: ', media_turnos)

executua_simulacoes(300)
