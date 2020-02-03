import random


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
