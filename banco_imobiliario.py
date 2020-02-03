import random
from saida.marcador import Marcador, executa_simulacoes
from modelo.comportamento import (
    Impulsivo,
    Exigente,
    Cauteloso,
    Aleatorio
)
from regra.item_jogo import Propriedade, Jogador

CASAS_TABULEIRO = 20


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
