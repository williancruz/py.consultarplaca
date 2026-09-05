from http_client import APIConnector


class ConsultasFinanceiras:

    def __init__(self, conector: APIConnector) -> None:
        self._conn = conector

    def consultar_infracoes_renainf(self, placa: str) -> dict:
        resposta = self._conn._request("GET", "/consultarRegistrosInfracoesRenainf",
                                       params={"placa": placa})
        return resposta.json()

    def consultar_alienacao_financeira(self, placa: str) -> dict:
        resposta = self._conn._request("GET",
                                       "/consultarGravame",
                                       params={"placa": placa})
        return resposta.json()

    def consultar_precos_fipe(self, placa: str) -> dict:
        resposta = self._conn._request("GET", "/consultarPrecoFipe",
                                       params={"placa": placa})
        return resposta.json()

    def consultar_leilao_prime(self, placa: str) -> dict:
        resposta = self._conn._request("GET",
                                       "/consultarRegistroLeilaoPrime",
                                       params={"placa": placa})
        return resposta.json()
