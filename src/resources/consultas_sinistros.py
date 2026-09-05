from http_client import APIConnector as conn


def consultar_perda_total(placa: str) -> dict:
    resposta = conn._request("GET",
                             "/consultarSinistroComPerdaTotal",
                             params={"placa": placa})
    return resposta.json()


def consultar_hist_roubo_furto(placa: str) -> dict:
    resposta = conn._request("GET",
                             "/consultarHistoricoRouboFurto",
                             params={"placa": placa})
    return resposta.json()
