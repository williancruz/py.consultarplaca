from dataclasses import dataclass, field
from utils import _FromDictMixin, _navegar_json, _parse_valor_brl


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


# =============================================================================
# CONSULTA DE DÉBITOS POR INFRAÇÕES — RENAINF
# =============================================================================
@dataclass
class _Infracao(_FromDictMixin):
    infracao: str = ""
    numero_auto_infracao: str = ""
    valor_aplicado: float = 0.0
    orgao_autuador: str = ""
    tipo_auto_infracao: str = ""
    local_infracao: str = ""
    municipio: str = ""
    unidade_medida: str = ""
    limite_permitido: str = ""
    medicao_considerada: str = ""
    medicao_real: str = ""
    data_hora_infracao: str = ""
    data_cadastramento: str = ""
    data_notificacao: str = ""
    data_emissao_penalidade: str = ""

    @classmethod
    def from_api_response(cls, item: dict):
        # junta os 3 sub-dicts num só e deixa o FromDictMixin resolver
        flat: dict = {
            **item.get("dados_infracao", {}),
            **item.get("aplicacao", {}),
            **item.get("eventos", {}),
        }
        infracao = cls.from_dict(flat)
        infracao.valor_aplicado = _parse_valor_brl(flat.get("valor_aplicado"))
        return infracao


@dataclass
class RegistroInfracoes:
    possui_infracoes: bool = False
    infracoes: list[_Infracao] = field(default_factory=list)

    @classmethod
    def from_api_response(cls, resposta_api: dict):
        _PATH: tuple = ("dados",
                        "registro_debitos_por_infracoes_renainf",
                        "infracoes_renainf")
        dados: dict = _navegar_json(resposta_api, _PATH)

        if dados.get("possui_infracoes") == "sim":
            infracoes: list[_Infracao] = []

            for item in dados.get("infracoes", []):
                infracoes.append(_Infracao.from_api_response(item))

            return cls(possui_infracoes=True, infracoes=infracoes)
        elif dados.get("possui_infracoes") == "nao":
            return False
        else:
            pass


# =============================================================================
# CONSULTA DE HISTÓRICO DE ROUBO/FURTO
# =============================================================================
@dataclass
class _BoletimOcorrencia(_FromDictMixin):
    boletim_ocorrencia: str = ""
    data_boletim_ocorrencia: str = ""
    tipo_ocorrencia: str = ""
    uf_ocorrencia: str = ""


@dataclass
class RegistroRouboFurto:
    possui_registro: bool | None = None
    registros: list[_BoletimOcorrencia] = field(default_factory=list)

    @classmethod
    def from_api_response(cls, resposta_api: dict):
        _PATH: tuple = ("dados", "historico_roubo_furto",
                        "registros_roubo_furto")
        dados: dict = _navegar_json(resposta_api, _PATH)

        if dados.get("possui_registro") == "sim":
            registros: list[_BoletimOcorrencia] = []

            for item in dados.get("registros", []):
                registros.append(_BoletimOcorrencia.from_dict(item))

            return cls(possui_registro=True, registros=registros)
        elif dados.get("possui_registro") == "nao":
            return cls(possui_registro=False)
        elif dados.get("possui_registro") == "indisponivel":
            return cls(possui_registro=None)
        else:
            pass
