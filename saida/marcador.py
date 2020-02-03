
SILENCIAR = True


class Marcador:

    @staticmethod
    def cobra_aluguel(func):
        if SILENCIAR:
            return func
        def wrapper(*args, **kw):
            casa = args[0]
            jogador = args[1]
            print('\t(-) {} paga aluguel da casa {} para {} no valor de {:.2f}'.format(
                jogador.comportamento.__class__.__name__,
                casa.numero,
                casa.dono.comportamento.__class__.__name__,
                casa.valor_aluguel
            ))
            return func(*args, **kw)
        return wrapper

    @staticmethod
    def realiza_compra(func):
        if SILENCIAR:
            return func
        def wrapper(*args, **kw):
            jogador = args[0]
            casa = args[1]
            print('\t[+] Casa {} vendida para {}: Saldo = {:.2f} - {:.2f}'.format(
                casa.numero,
                jogador.comportamento.__class__.__name__,
                jogador.saldo,
                casa.custo_venda,
            ))
            return func(*args, **kw)
        return wrapper

    @staticmethod
    def proxima_rodada(func):
        if SILENCIAR:
            return func
        def wrapper(*args, **kw):
            jogo = args[0]
            if len(args) > 1:
                numero_jogo = args[1]
                print('{} JOGO {} {}'.format(
                    '='*50,
                    numero_jogo,
                    '='*50,
            ))
            func(*args, **kw)
            print('--------- Rodada {} ------------'.format(jogo.rodada))
        return wrapper

    @staticmethod
    def fim_de_jogo(func):
        if SILENCIAR:
            return func
        def wrapper(*args, **kw):
            jogo = args[0]
            motivo = args[1]
            vencedor = func(*args, **kw)
            print('\t</> ***** Fim de jogo \t\t{} venceu por {}\t{}'.format(
                vencedor.comportamento.__class__.__name__,
                motivo,
                '_'*20
            ))
            return vencedor
        return wrapper

    @staticmethod
    def remove_jogador(func):
        if SILENCIAR:
            return func
        def wrapper(*args, **kw):
            perdedor = args[1]
            print('\t{!}','Jogador {} removido do jogo.'.format(
                perdedor.comportamento.__class__.__name__
            ))
            func(*args, **kw)
        return wrapper

    @staticmethod
    def ganha_bonus(func):
        if SILENCIAR:
            return func
        def wrapper(*args, **kw):
            jogador = args[0]
            valor = args[1]
            print('\t @  {} completou +1 volta: Saldo = {:.2f} + {:.2f}'.format(
                jogador.comportamento.__class__.__name__,
                jogador.saldo,
                valor
            ))
            func(*args, **kw)
        return wrapper
