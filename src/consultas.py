from http_client import APIConnector

__all__ = ["ConsultasCadastrais", "ConsultasFinanceiras", "ConsultasSinistros"]

class ConsultasCadastrais:
    def __init__(self, conector: APIConnector) -> None:
        self._conn = conector

    def consultar_saldo_creditos(self, ) -> dict:
        resposta = self._conn._request("GET", 
                                       "/consultarSaldo",
                                       params={})
        return resposta.json()

    def consultar_por_placa(self, placa: str) -> dict:
        resposta = self._conn._request("GET", 
                                       "/consultarPlaca",
                                       params={"placa": placa})
        return resposta.json()

    def consultar_por_chassi(self, chassi: str) -> dict:
        resposta = self._conn._request("GET", 
                                       "/consultarChassi",
                                       params={"chassi": chassi})
        return resposta.json()

    def consultar_nro_renavam(self, placa: str) -> dict:
        resposta = self._conn._request("GET", 
                                       "/consultarRenavam",
                                       params={"placa": placa})
        return resposta.json()

    def consultar_proprietario_atual(self, placa: str) -> dict:
        resposta = self._conn._request("GET", 
                                       "/consultarProprietarioAtual",
                                       params={"placa": placa})
        return resposta.json()


class ConsultasFinanceiras:
    def __init__(self, conector: APIConnector) -> None:
        self._conn = conector

    def consultar_infracoes_renainf(self, placa: str) -> dict:
        resposta = self._conn._request("GET", 
                                       "/consultarRegistrosInfracoesRenainf",
                                       params={"placa": placa})
        return resposta.json()

    def consultar_alienacao_financeira(self, placa: str) -> dict:
        resposta = self._conn._request("GET",
                                       "/consultarGravame",
                                       params={"placa": placa})
        return resposta.json()

    def consultar_precos_fipe(self, placa: str) -> dict:
        resposta = self._conn._request("GET", 
                                       "/consultarPrecoFipe",
                                       params={"placa": placa})
        return resposta.json()

    def consultar_leilao_prime(self, placa: str) -> dict:
        resposta = self._conn._request("GET",
                                       "/consultarRegistroLeilaoPrime",
                                       params={"placa": placa})
        return resposta.json()


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
