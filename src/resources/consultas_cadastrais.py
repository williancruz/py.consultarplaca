from http_client import APIConnector as conn


def consultar_saldo_creditos() -> dict:
    resposta = conn._request("GET", "/consultarSaldo")
    return resposta.json()


def consultar_por_placa(placa: str) -> dict:
    resposta = conn._request("GET", "/consultarPlaca",
                             params={"placa": placa})
    return resposta.json()


def consultar_por_chassi(chassi: str) -> dict:
    resposta = conn._request("GET", "/consultarChassi",
                             params={"chassi": chassi})
    return resposta.json()


def consultar_nro_renavam(placa: str) -> dict:
    resposta = conn._request("GET", "/consultarRenavam",
                             params={"placa": placa})
    return resposta.json()


def consultar_proprietario_atual(placa: str) -> dict:
    resposta = conn._request("GET", "/consultarProprietarioAtual",
                             params={"placa": placa})
    return resposta.json()
