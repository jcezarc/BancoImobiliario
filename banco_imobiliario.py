import random

class Sequencia:
    def __init__(self):
        self.proximo = None 
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
                ultimo.proximo = elemento
            ultimo = elemento
            lista.append(elemento)
        ultimo.proximo = primeiro
        return primeiro, lista

class Propriedade(Sequencia):
    """
    Uma propriedade é um imóvel ocupando
    uma posição (ou `casa`) no tabuleiro
    :numero é como se fosse a numeração da rua 
            (para debug/logging...)
    :valor_venda recebe um valor qualquer, apenas como exemplo
    :valor_aluguel  vale 0.5% do `valor_venda`
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
    def decide_compra(propriedade):
        deve_comprar = self.comportamento.deve_comprar(
            propriedade,
            self
        )
        if deve_comprar:
            self.saldo -= propriedade.valor_venda
            propriedade.dono = self
    def paga_aluguel(propriedade):
        valor = propriedade.valor_aluguel
        self.saldo -= valor
        propriedade.dono.ganha_bonus(valor)
    def ganha_bonus(valor):
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
    def deve_comprar(propriedade, jogador):
        return True

class Exigente:
    def deve_comprar(propriedade, jogador):
        return propriedade.valor_aluguel > 50

class Cauteloso:
    def deve_comprar(propriedade, jogador):
        reserva = self.saldo - propriedade.valor_venda
        return reserva >= 80

class Aleatorio:
    def deve_comprar(propriedade, jogador):
        return bool(random.getrandbits(1))
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
        self.turnos = 0
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
        def proximo_turno(self):
            if not self.jogadores_ativos:
                raise Exception('Nenhum jogador ativo')
            self.jogador.move(random.randint(1, 6), self)
            self.jogador = self.jogador.proximo
            self.turnos += 1
        def remove_jogador(self, perdedor):
            self.jogadores_ativos.remove(perdedor)
            for casa in self.tabuleiro:
                if casa.dono == perdedor:
                    casa.dono = None
        def encerra_jogo(self):
            vencedor = None
            for jogador in self.jogadores_ativos:
                if not vencedor or jogador.saldo > vencedor.saldo:
                    vencedor = jogador
            return vencedor

def executua_simulacao():
    jogo = Jogo()