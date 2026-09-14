from dataclasses import dataclass, field
from utils import _FromDictMixin, _navegar_json, _parse_flt


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

# =============================================================================
# CONSULTA DE PLACA/CHASSI/RENAVAM
# =============================================================================


@dataclass
class DadosVeiculo(_FromDictMixin):
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
class DadosTecnicos(_FromDictMixin):
    tipo_veiculo: str = ""
    sub_segmento: str = ""
    numero_motor: str = ""
    numero_caixa_cambio: str = ""
    potencia: str = ""
    cilindradas: str = ""


@dataclass
class DadosCarga(_FromDictMixin):
    numero_eixos: str = ""
    capacidade_maxima_tracao: str = ""
    capacidade_passageiro: str = ""


@dataclass
class Veiculo(_FromDictMixin):
    dados_veiculo: DadosVeiculo = field(default_factory=DadosVeiculo)
    dados_tecnicos: DadosTecnicos = field(default_factory=DadosTecnicos)
    dados_carga: DadosCarga = field(default_factory=DadosCarga)

# =============================================================================
# CONSULTA DE PROPRIETÁRIO
# =============================================================================


@dataclass
class Proprietario(_FromDictMixin):
    nome: str = ""
    documento: str = ""
    tipo_documento: str = ""


# =============================================================================
# CONSULTA DE SINISTRO COM PERDA TOTAL
# =============================================================================
@dataclass
class RegistroPerdaTotal(_FromDictMixin):
    possui_registro: bool | None = None
    registro: str = ""


# =============================================================================
# CONSULTA DE DÉBITOS POR INFRAÇÕES — RENAINF
# =============================================================================
@dataclass
class Infracao(_FromDictMixin):
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


@dataclass
class RegistroInfracoes(_FromDictMixin):
    possui_infracoes: bool = False
    infracoes: list[Infracao] = field(default_factory=list)


# =============================================================================
# CONSULTA DE HISTÓRICO DE ROUBO/FURTO
# =============================================================================
@dataclass
class BoletimOcorrencia(_FromDictMixin):
    boletim_ocorrencia: str = ""
    data_boletim_ocorrencia: str = ""
    tipo_ocorrencia: str = ""
    uf_ocorrencia: str = ""


@dataclass
class RegistroRouboFurto(_FromDictMixin):
    possui_registro: bool | None = None
    registros: list[BoletimOcorrencia] = field(default_factory=list)


# =============================================================================
# CONSULTA DE PREÇOS FIPE
# =============================================================================
@dataclass
class InfoFipe(_FromDictMixin):
    codigo_fipe: str = ""
    modelo_versao: str = ""
    preco: float = 0.0
    mes_referencia: str = ""
    historico: dict = field(default_factory=dict)


@dataclass
class PrecosFipe(_FromDictMixin):
    veiculo: Veiculo = field(default_factory=Veiculo)
    informacoes_fipe: list[InfoFipe] = field(default_factory=list)
