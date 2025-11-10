import unicodedata
import json
from flask import jsonify

def remover_acentos(texto):
    # Normaliza o texto para decompor os caracteres com acentos
    texto_normalizado = unicodedata.normalize('NFD', texto)
    # Remove os acentos e retorna o texto sem eles, convertido para maiúsculas
    return ''.join(c for c in texto_normalizado if not unicodedata.combining(c)).upper()

def remover_acentos_dict(dicionario):
    novo_dicionario = {}
    for chave, valor in dicionario.items():
        if isinstance(valor, str):
            novo_dicionario[chave] = remover_acentos(valor)
        elif isinstance(valor, dict):
            novo_dicionario[chave] = remover_acentos_dict(valor)
        else:
            novo_dicionario[chave] = valor
    return json.dumps(novo_dicionario, indent=4)

if __name__ == '__main__':
    Cadastro = {
        "Nome do Item": "PNEU",
        "Descricao Comercial": "PNEU 205/65R17",
        "Fabricante / Marca": "MICHELIN",
        "Código Fabricante": "123456",
        "uso": "UTILIZADO EM SUVS MÉDIAS CAÇADAS Á COMO POR EXÊMPLÓ: TIGGO 7, KICKS, T-CROSS",
        "Detalhes do Item": {
            "largura": "205",
            "perfil": "65",
            "diametro": "17",
            "indiceCarga": "91",
            "simboloVelocidade": "V"
        }
    }
    Cadastro_sem_acentos = remover_acentos_dict(Cadastro)
    print(type(Cadastro_sem_acentos))
    print(Cadastro_sem_acentos)