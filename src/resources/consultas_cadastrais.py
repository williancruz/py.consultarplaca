from http_client import APIConnector


class ConsultasCadastrais:

    def __init__(self, conector: APIConnector) -> None:
        self._conn = conector

    def consultar_saldo_creditos(self, ) -> dict:
        resposta = self._conn._request("GET", "/consultarSaldo")
        return resposta.json()

    def consultar_por_placa(self, placa: str) -> dict:
        resposta = self._conn._request("GET", "/consultarPlaca",
                                       params={"placa": placa})
        return resposta.json()

    def consultar_por_chassi(self, chassi: str) -> dict:
        resposta = self._conn._request("GET", "/consultarChassi",
                                       params={"chassi": chassi})
        return resposta.json()

    def consultar_nro_renavam(self, placa: str) -> dict:
        resposta = self._conn._request("GET", "/consultarRenavam",
                                       params={"placa": placa})
        return resposta.json()

    def consultar_proprietario_atual(self, placa: str) -> dict:
        resposta = self._conn._request("GET", "/consultarProprietarioAtual",
                                       params={"placa": placa})
        return resposta.json()
