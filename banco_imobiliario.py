import random
from marcador import Marcador, executa_simulacoes

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
    :custo_venda recebe um valor qualquer, apenas como exemplo
    :valor_aluguel  recebe um valor parecido, só que menor..
    """
    def __init__(self, numero):
        self.numero = numero
        self.custo_venda = random.randrange(100, 200)
        self.valor_aluguel = random.randrange(30, 90)
        self.dono = None
        
    @Marcador.cobra_aluguel
    def cobra_aluguel(self, jogador):
        jogador.saldo -= self.valor_aluguel
        self.dono.saldo += self.valor_aluguel


class Jogador(ItemJogo):

    def __init__(self, comportamento):
        self.comportamento = comportamento()
        self.saldo = 300
        self.posicao = 0

    @Marcador.realiza_compra
    def realiza_compra(self, propriedade):
        self.saldo -= propriedade.custo_venda
        propriedade.dono = self
    
    def decide_compra(self, propriedade):
        if self.saldo < propriedade.custo_venda:
            return False
        return self.comportamento.deve_comprar(
            propriedade,
            self
        )

    @Marcador.ganha_bonus
    def ganha_bonus(self, valor):
        self.saldo += valor

    def movimenta(self, distancia, jogo):
        """
        Aqui `casa` também é uma Propriedade,
        mas é tratada como um espaço no tabuleiro
        """
        idx = self.posicao + distancia
        if idx >= CASAS_TABULEIRO:
            self.ganha_bonus(100) #--- Completou uma volta!
            idx %= CASAS_TABULEIRO
        casa = jogo.tabuleiro[idx]
        if casa.dono:
            if casa.dono != self:
                casa.cobra_aluguel(self)
            if self.saldo < 0:
                jogo.remove_jogador(self)
        elif self.decide_compra(casa):
            self.realiza_compra(casa)
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

    @Marcador.proxima_rodada
    def __init__(self, numero, limite_rodadas):
        """
        Cria o tabuleiro e
        Também cria 4 jogadores,
        um de cada comportamento
        """
        self.rodada = 1
        self.motivo = ''
        self.tabuleiro = Propriedade.get_elementos(
            range(1, CASAS_TABULEIRO + 1)
        )
        self.jogadores_ativos = Jogador.get_elementos([
            Impulsivo,
            Exigente,
            Cauteloso,
            Aleatorio
        ])
        self.idx_jogador = 0 #-- Jogador atual
        self.limite_rodadas = limite_rodadas

    @Marcador.proxima_rodada
    def proxima_rodada(self):
        self.rodada += 1

    def atualiza(self):
        if not self.jogadores_ativos:
            raise Exception('Nenhum jogador ativo')
        elif len(self.jogadores_ativos) == 1:
            return self.fim_de_jogo('WO')
            #      ^^^---- vitória por W.O.
        idx = self.idx_jogador
        jogador = self.jogadores_ativos[idx]
        jogador.movimenta(random.randint(1, 6), self)
        idx += 1
        if idx >= len(self.jogadores_ativos):
            self.proxima_rodada()
            if self.rodada >= self.limite_rodadas:
                return self.fim_de_jogo('TimeOut')
            idx = 0
        self.idx_jogador = idx
        return None

    @Marcador.remove_jogador
    def remove_jogador(self, perdedor):
        for casa in self.tabuleiro:
            if casa.dono == perdedor:
                casa.dono = None
        self.jogadores_ativos.remove(perdedor)

    @Marcador.fim_de_jogo
    def fim_de_jogo(self, motivo):
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


executa_simulacoes(Jogo, 10)
