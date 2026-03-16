import json


def salvar_score(nome, kills):
    dados = ler_scores()
    dados.append({"nome": nome, "kills": kills})

    with open("scores.json", "w") as arquivo:
        json.dump(dados, arquivo)


def ler_scores():
    try:
        with open("scores.json", "r") as arquivo:
            lista = json.load(arquivo)
            return sorted(lista, key=lambda x: x['kills'], reverse=True)
    except:
        return []
