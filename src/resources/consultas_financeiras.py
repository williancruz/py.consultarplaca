from http_client import APIConnector as conn

def consultar_infracoes_renainf(placa: str) -> dict:
    resposta = conn._request("GET", "/consultarRegistrosInfracoesRenainf",
                                params={"placa": placa})
    return resposta.json()

def consultar_alienacao_financeira(placa: str) -> dict:
    resposta = conn._request("GET",
                                "/consultarGravame",
                                params={"placa": placa})
    return resposta.json()

def consultar_precos_fipe(placa: str) -> dict:
    resposta = conn._request("GET", "/consultarPrecoFipe",
                                params={"placa": placa})
    return resposta.json()

def consultar_leilao_prime(placa: str) -> dict:
    resposta = conn._request("GET",
                                "/consultarRegistroLeilaoPrime",
                                params={"placa": placa})
    return resposta.json()