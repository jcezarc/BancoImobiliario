import sys
import random
sys.path.append('..')
from saida.marcador import Marcador

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
        qt_casas = len(jogo.tabuleiro)
        if idx >= qt_casas:
            self.ganha_bonus(100) #--- Completou uma volta!
            idx %= qt_casas
        casa = jogo.tabuleiro[idx]
        if casa.dono:
            if casa.dono != self:
                casa.cobra_aluguel(self)
            if self.saldo < 0:
                jogo.remove_jogador(self)
        elif self.decide_compra(casa):
            self.realiza_compra(casa)
        self.posicao = idx
