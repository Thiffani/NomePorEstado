import requests
from pprint import pprint
import matplotlib.pyplot as plt

def obter_request(url, params = None):
    """Faz uma requisição get e retorna em JSON"""
    
    try:
        response = requests.get(url, params = params)
        response.raise_for_status()
        return response.json()

    except requests.HTTPError as e:
        print(f"Erro no request: {e}")
        return None
     
def frequencia_nome(name):
    """Obtém um dicionário de frequencia de nomes por estado no formato {id_estado: frequencia}"""
    url = f"https://servicodados.ibge.gov.br/api/v2/censos/nomes/{name}"
    dados_frequencia = obter_request(url, params={"groupBy": "UF"}) or []
    return {int (dado["localidade"]): dado["res"][0]["proporcao"] for dado in dados_frequencia}

def busca_id_estado():
    """Obtém um dicionário de estados no formato {id_estado: Nome_estado}"""
    url = "https://servicodados.ibge.gov.br/api/v1/localidades/estados"
    dados_estados = obter_request(url, params= {"view": "nivelado"}) or []
    return {estado["UF-id"]: estado["UF-sigla"] for estado in dados_estados}

def criar_grafico(estados, frequencia, name):
    """Cria um gráfico com os dados obtidos"""
    ordenado = sorted(frequencia.items(), key=lambda item: item[1], reverse=True)

    nomes_estados = [estados.get(id_estado, "Desconhecido") for id_estado, _ in ordenado]
    valores = [valor for _, valor in ordenado]

    plt.figure(figsize=(10, 6))
    plt.bar(nomes_estados, valores, color='skyblue')
    plt.xlabel("Proporção (por 100.000 habitantes)")
    plt.ylabel("Estado", fontsize=10) 
    plt.title(f"Frequência do nome '{name}' por estado (IBGE)")
    plt.show()

    
def main(name):
    dict_estados = busca_id_estado()
    dict_frequencia = frequencia_nome(name)
    criar_grafico(dict_estados, dict_frequencia, name)


if __name__ == "__main__":
    nome = input("Digite um nome: ")
    main(nome.upper())
    