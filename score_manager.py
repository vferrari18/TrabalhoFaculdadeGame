import json  # Importa a biblioteca para manipular arquivos de dados estruturados


def salvar_score(nome, kills):  # Função que recebe o nome do jogador e o total de mortes causadas
    dados = ler_scores()  # Chama a função de leitura para pegar o que já existe no arquivo
    dados.append({"nome": nome, "kills": kills})  # Adiciona um novo "dicionário" com os dados da partida atual

    # Abre o arquivo 'scores.json' no modo 'w' (write/escrita)
    with open("scores.json", "w") as arquivo:
        # Transforma a lista de nomes e pontos em texto e salva no arquivo físico
        json.dump(dados, arquivo)


def ler_scores():  # Função que busca as pontuações guardadas no computador
    try:  # Tenta executar o bloco abaixo (caso o arquivo já exista)
        with open("scores.json", "r") as arquivo:  # Abre o arquivo no modo 'r' (read/leitura)
            # Converte o texto do arquivo de volta para uma lista do Python
            lista = json.load(arquivo)
            # Ordena a lista: olha para 'kills' e coloca o maior valor primeiro (reverse=True)
            return sorted(lista, key=lambda x: x['kills'], reverse=True)
    except:  # Se o arquivo não existir (primeira vez que o jogo roda), cai aqui
        return []  # Retorna uma lista vazia para não travar o programa