from http_client import APIConnector


class ConsultasSinistros:

    def __init__(self, conector: APIConnector) -> None:
        self._conn = conector

    def consultar_perda_total(self, placa: str) -> dict:
        resposta = self._conn._request("GET",
                                       "/consultarSinistroComPerdaTotal",
                                       params={"placa": placa})
        return resposta.json()

    def consultar_hist_roubo_furto(self, placa: str) -> dict:
        resposta = self._conn._request("GET",
                                       "/consultarHistoricoRouboFurto",
                                       params={"placa": placa})
        return resposta.json()
