from dataclasses import dataclass, field
from utils import _FromDictMixin, _navegar_json


# =============================================================================
# CONSULTA DE GRAVAME
# =============================================================================


@dataclass
class RegistroGravame(_FromDictMixin):
    possui_gravame: bool | None = None
    financeira_cnpj: str = ""
    financeira_nome: str = ""
    data_registro: str = ""
    placa: str = ""
    chassi: str = ""
    uf_placa: str = ""
    situacao: str = ""

    @classmethod
    def from_api_response(cls, resposta_api: dict):
        _PATH: tuple = ("dados", "gravame")
        dados: dict = _navegar_json(resposta_api, _PATH)

        if dados.get("possui_gravame") == "sim":
            registro = _navegar_json(dados, "registro")
            financeira = _navegar_json(registro, "agente_financeiro")

            return cls(
                possui_gravame=True,
                financeira_cnpj=financeira.get("cnpj"),
                financeira_nome=financeira.get("nome"),
                data_registro=registro.get("data_registro"),
                placa=registro.get("placa"),
                chassi=registro.get("chassi"),
                uf_placa=registro.get("uf_placa"),
                situacao=registro.get("situacao"),
            )
        elif dados.get("possui_gravame") == "nao":
            return cls(possui_gravame=False)
        elif dados.get("possui_gravame") == "indisponivel":
            return cls(possui_gravame=None)
        else:
            pass


# =============================================================================
# CONSULTA DE PLACA/CHASSI/RENAVAM
# =============================================================================


@dataclass
class _DadosVeiculo(_FromDictMixin):
    placa: str = ""
    chassi: str = ""
    ano_fabricacao: str = ""
    ano_modelo: str = ""
    marca: str = ""
    modelo: str = ""
    cor: str = ""
    segmento: str = ""
    especie: str = ""
    combustivel: str = ""
    procedencia: str = ""
    municipio: str = ""
    uf_municipio: str = ""
    renavam: str = ""


@dataclass
class _DadosTecnicos(_FromDictMixin):
    tipo_veiculo: str = ""
    sub_segmento: str = ""
    numero_motor: str = ""
    numero_caixa_cambio: str = ""
    potencia: str = ""
    cilindradas: str = ""


@dataclass
class _DadosCarga(_FromDictMixin):
    numero_eixos: str = ""
    capacidade_maxima_tracao: str = ""
    capacidade_passageiro: str = ""


@dataclass
class Veiculo:
    dados_veiculo: _DadosVeiculo = field(default_factory=_DadosVeiculo)
    dados_tecnicos: _DadosTecnicos = field(default_factory=_DadosTecnicos)
    dados_carga: _DadosCarga = field(default_factory=_DadosCarga)

    @classmethod
    def from_api_response(cls, resposta_api: dict):
        info = resposta_api.get("dados", {}).get("informacoes_veiculo", {})

        return cls(
            dados_veiculo=_DadosVeiculo.from_dict(info.get("dados_veiculo")),
            dados_tecnicos=_DadosTecnicos.from_dict(info.get("dados_tecnicos")),
            dados_carga=_DadosCarga.from_dict(info.get("dados_carga")),
        )


# =============================================================================
# CONSULTA DE PROPRIETÁRIO
# =============================================================================

@dataclass
class Proprietario:
    nome: str = ""
    doc_mascarado: str = ""
    tipo_documento: str = ""

    @classmethod
    def from_api_response(cls, resposta_api: dict):
        _PATH: tuple = ("dados", "proprietario_atual")
        dados: dict = _navegar_json(resposta_api, _PATH)

        return cls(
            nome=dados.get("nome"),
            doc_mascarado=dados.get("documento"),
            tipo_documento=dados.get("tipo_documento")
        )


# =============================================================================
# CONSULTA DE SINISTRO COM PERDA TOTAL
# =============================================================================
@dataclass
class RegistroPerdaTotal:
    possui_registro: bool | None = None
    registro: str = ""

    @classmethod
    def from_api_response(cls, resposta_api: dict) -> dict:
        _PATH: tuple = ("dados", "registro_sinistro_com_perda_total")
        dados: dict = _navegar_json(resposta_api, _PATH)

        if dados["possui_registro"] == "sim":
            return cls(
                possui_registro=True,
                registro=dados.get("registro")
            )
        elif dados["possui_registro"] == "nao":
            return cls(possui_registro=False)
        elif dados["possui_registro"] == "indisponivel":
            return cls(possui_registro=None)
        else:
            pass
