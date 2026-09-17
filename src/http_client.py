import httpx


class APIConnector():
    def __init__(self, email: str, api_key: str) -> None:
        transport = httpx.HTTPTransport(retries=3)

        self._session = httpx.Client(
            base_url="https://api.consultarplaca.com.br/v2",
            auth=(email, api_key),
            headers={
                "Accept": "application/json",
                "User-Agent": "PyConsultarPlacasLib/Alpha",
            },
            transport=transport,
            timeout=10.0
        )

    def _request(self, metodo: str, rota: str, **kwargs) -> httpx.Response:
        if not rota.startswith("/"):
            rota = f"/{rota}"

        try:
            resposta = self._session.request(method=metodo,
                                             url=rota,
                                             **kwargs)
            resposta.raise_for_status()
            return resposta
        except:
            pass
