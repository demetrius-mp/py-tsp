from metaheuristicas import HillClimbing, SimulatedAnnealing
from metaheuristicas.utils import Grafo
import os


def suppress_qt_warnings():
    os.environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    os.environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    os.environ["QT_SCALE_FACTOR"] = "1"


def is_type(tipo, valor):
    try:
        tipo(valor)
        return True
    except ValueError:
        return False


def pega_parametro(mensagem, tipo: type = float):
    param = input(mensagem)
    while not is_type(tipo, param):
        param = input('Por favor, digite um valor válido: ')

    return tipo(param)


def mostra_metaheuristicas():
    print('Metaheurísticas:')
    print('\t1. Simulated Annealing')
    print('\t2. Hill Climbing')
    print()


def mostra_arquivos():
    arquivos = os.listdir('dados')
    arquivos.remove('solucoes.txt')
    for idx, arquivo in enumerate(arquivos):
        if idx % 3 == 0 and idx != 0:
            print()
        if idx == 6:
            print(f'{idx}. {arquivo}', end='\t\t')
            continue

        print(f'{idx}. {arquivo}', end='\t\t\t')

    return arquivos


def pega_arquivo(arquivos):
    idx_arquivo = int(input('Digite o número correspondente ao caso de teste desejado: '))
    if idx_arquivo not in list(range(len(arquivos))):
        idx_arquivo = input('Por favor, digite uma opção válida: ')

    return arquivos[idx_arquivo]


def inicializa():
    arquivos = mostra_arquivos()
    print('\n')
    arquivo = pega_arquivo(arquivos)
    grafo = Grafo(f'dados/{arquivo}')
    grafo.ler_vertices()

    return grafo


def finaliza(grafo, instancia, distancia):
    melhores_solucoes = {
        'att48': 10628,
        'berlin52': 7542,
        'bier127': 118282,
        'eil76': 538,
        'eil101': -1,
        'kroA100': 21282,
        'kroE100': 22068,
        'pr76': 108159,
        'rat99': 1211,
        'st70': 675,
    }
    melhor_dist = melhores_solucoes[instancia]

    print(f'Distância percorrida: {round(distancia)}')
    print(f'Melhor distância para esta instância: {melhor_dist}')
    print(f'Diferença: {round(distancia - melhor_dist)}')

    print()

    ver_figura = input('Deseja ver a figura com a soluçao (s/n)? ')
    while ver_figura not in ('s', 'n'):
        ver_figura = input('Por favor, digite um valor válido (s/n): ')

    if ver_figura == 's':
        fig = grafo.desenhar_solucao()
        fig.show()


def simulated_annealing():
    print()
    print('\t\t\t\t  ===== Simulated Annealing =====')

    grafo = inicializa()
    instancia = grafo.entrada.split('/')[-1][:-8]

    print()
    print('===== Simulated Annealing: Definição de parâmetros =====')
    msg = '(casa decimal separada por .)'

    t_max = pega_parametro(f'Temperatura máxima {msg}: ')
    tx_resfria = pega_parametro(f'Taxa de resfriamento {msg}: ')
    t_min = pega_parametro(f'Temperatura mínima {msg}: ')
    max_iter = pega_parametro(f'Máximo de iterações: ', tipo=int)
    print()

    sa = SimulatedAnnealing(grafo, t_max, tx_resfria, t_min, max_iter)
    solucao, distancia = sa.run()

    finaliza(sa.grafo, instancia, distancia)


def hill_climbing():
    print()
    print('\t\t\t\t  ===== Hill Climbing =====')

    grafo = inicializa()
    instancia = grafo.entrada.split('/')[-1][:-8]

    print('===== Hill Climbing: Definição de parâmetros =====')

    max_iter = pega_parametro(f'Máximo de iterações (0 para infinito): ')
    print()

    hc = HillClimbing(grafo, max_iter)
    solucao, distancia = hc.run()

    finaliza(hc.grafo, instancia, distancia)


def main():
    print('=== Trabalho final - Implementação algorítmica ===')
    mostra_metaheuristicas()
    option = input('Digite o número referente a metaheurística desejada: ')
    while option not in ('1', '2'):
        option = input('Por favor, digite uma opção válida: ')

    if option == '1':
        simulated_annealing()

    if option == '2':
        hill_climbing()


if __name__ == '__main__':
    suppress_qt_warnings()
    main()
