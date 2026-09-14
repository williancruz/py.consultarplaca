from utils import _navegar_json, _parse_flt
from http_client import APIConnector
from modelos import *
from consultas import *
from exceptions import *


def _checar_dados_basicos(dados: dict):
    # 1. Pega apenas a chave "informacoes_veiculo" para tratamento
    dados: dict = _navegar_json(dados, ("dados", "informacoes_veiculo"))

    # 2. Verifica se chave obrigatória "dados_veiculo" existe e não nula
    if "dados_veiculo" not in dados:
        raise CampoAusenteErro()

    if dados.get("dados_veiculo") is None:
        raise CampoVazioErro()

    dados_veiculo: dict = dados.get("dados_veiculo")

    # Na rota /consultarPrecoFipe, o campo que contém o ano de fabricação
    # está escrito errado. Vamos corrigir isso antes de prosseguir.
    if "ano_frabricacao" in dados_veiculo:
        dados_veiculo["ano_fabricacao"] = dados_veiculo.pop("ano_frabricacao")

    # 3. Verifica se chave obrigatória "dados_tecnicos" existe e não nula
    if "dados_tecnicos" not in dados:
        raise CampoAusenteErro()

    if dados.get("dados_tecnicos") is None:
        raise CampoVazioErro()

    dados_tecnicos: dict = dados.get("dados_tecnicos")

    # 4. Verifica se chave obrigatória "dados_carga" existe e não nula
    if "dados_carga" not in dados:
        raise CampoAusenteErro()

    if dados.get("dados_carga") is None:
        raise CampoVazioErro()

    dados_carga: dict = dados.get("dados_carga")

    return (dados_veiculo, dados_tecnicos, dados_carga)


class ConsultarPlacaClient():
    def __init__(self, email: str, token: str):
        __conector = APIConnector(email=email, api_key=token)
        self._ccad = ConsultasCadastrais(__conector)
        self._cfin = ConsultasFinanceiras(__conector)
        self._csin = ConsultasSinistros(__conector)

    def consultar_gravame(self, placa: str) -> RegistroGravame:
        # 1. Pega as informações da API
        raw = self._cfin.consultar_alienacao_financeira(placa)

        # 2. Pega apenas a chave "gravame" para tratamento
        dados: dict = _navegar_json(raw, ("dados", "gravame"))

        # 3. Verifica se chave obrigatória "possui_gravame" existe, se não é
        # nula ou se possui valor diferente do acordado na documentação
        if "possui_gravame" not in dados:
            raise CampoAusenteErro()

        if dados.get("possui_gravame") is None:
            raise CampoVazioErro()

        possui_gravame = dados.get("possui_gravame")

        if possui_gravame not in ("sim", "nao", "indisponivel"):
            raise ValorInvalidoErro("possui_gravame", possui_gravame)

        # 4. Converte o valor de "possui_gravame" para booleano ou None.
        # Isso permitirá que a aplicação consumidora da biblioteca possa
        # efetuar outros tratamentos de dados.
        if possui_gravame == "sim":
            dados["possui_gravame"] = True

            # 5. Verifica se a chave obrigatória "registro" existe, conforme
            # documentação da API. Também verifica se não é nula.
            if "registro" not in dados:
                raise CampoAusenteErro()

            registro = dados.get("registro")

            if registro is None:
                raise CampoVazioErro()

            # 6. Achata o dicionário "dados"
            dados["data_registro"] = registro.get("data_registro")
            dados["placa"] = registro.get("placa")
            dados["chassi"] = registro.get("chassi")
            dados["uf_placa"] = registro.get("uf_placa")
            dados["situacao"] = registro.get("situacao")

            agente_financeiro = registro.get("agente_financeiro")

            dados["financeira_cnpj"] = agente_financeiro.get("cnpj")
            dados["financeira_nome"] = agente_financeiro.get("nome")

            # 7. Descarta chave inutilizada
            dados.pop("registro")
        elif possui_gravame == "nao":
            dados["possui_gravame"] = False
        elif possui_gravame == "indisponivel":
            dados["possui_gravame"] = None

        # 9. Retornar objeto RegistroGravame tratado
        return RegistroGravame.from_dict(dados)

    def consultar_placa(self, placa: str) -> Veiculo:
        # 1. Pega as informações da API
        raw = self._ccad.consultar_por_placa(placa)

        # 2. Descompactar os blocos com os dados do Veículo
        a, b, c = _checar_dados_basicos(raw)

        # 3. Construir os subobjetos do Veiculo
        dados_veiculo = DadosVeiculo.from_dict(a)
        dados_tecnicos = DadosTecnicos.from_dict(b)
        dados_carga = DadosCarga.from_dict(c)

        # 4. Retorna o objeto "Veiculo" tratado
        return Veiculo.from_dict({
            "dados_veiculo": dados_veiculo,
            "dados_tecnicos": dados_tecnicos,
            "dados_carga": dados_carga
        })

    def consultar_chassi(self, chassi: str) -> Veiculo:
        # 1. Pega as informações da API
        raw = self._ccad.consultar_por_chassi(chassi)

        # 2. Descompactar os blocos com os dados do Veículo
        a, b, c = _checar_dados_basicos(raw)

        # 3. Construir os subobjetos do Veiculo
        dados_veiculo = DadosVeiculo.from_dict(a)
        dados_tecnicos = DadosTecnicos.from_dict(b)
        dados_carga = DadosCarga.from_dict(c)

        # 4. Retorna o objeto "Veiculo" construído
        return Veiculo.from_dict({
            "dados_veiculo": dados_veiculo,
            "dados_tecnicos": dados_tecnicos,
            "dados_carga": dados_carga
        })

    def consultar_renavam(self, placa: str) -> Veiculo:
        # 1. Pega as informações da API
        raw = self._ccad.consultar_nro_renavam(placa)

        # 2. Descompactar os blocos com os dados do Veículo
        a, b, c = _checar_dados_basicos(raw)

        # 3. Construir os subobjetos do Veiculo
        dados_veiculo = DadosVeiculo.from_dict(a)
        dados_tecnicos = DadosTecnicos.from_dict(b)
        dados_carga = DadosCarga.from_dict(c)

        # 4. Verificar se campo "renavam" obrigatório existe
        if "renavam" not in a:
            raise CampoAusenteErro()

        if a.get("renavam") is None:
            raise CampoVazioErro()

        # 5. Retorna o objeto "Veiculo" construído
        return Veiculo.from_dict({
            "dados_veiculo": dados_veiculo,
            "dados_tecnicos": dados_tecnicos,
            "dados_carga": dados_carga
        })

    def consultar_proprietario(self, placa: str) -> Proprietario:
        # 1. Pega as informações da API
        raw = self._ccad.consultar_proprietario_atual(placa)

        # 2. Pega apenas a chave "proprietario_atual" para tratamento
        dados = _navegar_json(raw, ("dados", "proprietario_atual"))

        # 3. Nenhum tratamento aqui, retornar objeto Proprietario
        return Proprietario.from_dict(dados)

    def consultar_perda_total(self, placa: str) -> RegistroPerdaTotal:
        # 1. Pega as informações da API
        raw = self._csin.consultar_perda_total(placa)

        # 2. Pega apenas a chave para tratamento
        dados = _navegar_json(raw, ("dados",
                                    "registro_sinistro_com_perda_total"))

        if "possui_registro" not in dados:
            raise CampoAusenteErro()

        possui_registro = dados.get("possui_registro")

        if possui_registro not in ("sim", "nao", "indisponivel"):
            raise ValorInvalidoErro("possui_registro", possui_registro)

        if possui_registro == "sim":
            dados["possui_registro"] = True
        elif possui_registro == "nao":
            dados["possui_registro"] = False
        elif possui_registro == "indisponivel":
            dados["possui_registro"] = None

        return RegistroPerdaTotal.from_dict(dados)

    def consultar_infracoes(self, placa: str):
        # 1. Pega as informações da API
        raw = self._cfin.consultar_infracoes_renainf(placa)

        # 2. Pega apenas a "infracoes_renainf" chave para tratamento
        dados = _navegar_json(raw, ("dados",
                                    "registro_debitos_por_infracoes_renainf",
                                    "infracoes_renainf"))

        if "possui_infracoes" not in dados:
            raise CampoAusenteErro()

        possui_infracoes = dados.get("possui_infracoes")

        if possui_infracoes not in ("sim", "nao", "indisponivel"):
            raise ValorInvalidoErro("possui_infracoes", possui_infracoes)

        if possui_infracoes == "sim":
            dados["possui_infracoes"] = True

            if "infracoes" not in dados:
                raise CampoAusenteErro()

            if dados.get("possui_infracoes") is None:
                raise CampoVazioErro()

            lista_infracoes: list[Infracao] = []

            for infracao in dados.get("infracoes"):
                flat: dict = {
                    **infracao.get("dados_infracao", {}),
                    **infracao.get("aplicacao", {}),
                    **infracao.get("eventos", {}),
                }

                flat["valor_aplicado"] = _parse_flt(flat.get("valor_aplicado"))

                lista_infracoes.append(Infracao.from_dict(flat))
        elif possui_infracoes == "nao":
            dados["possui_infracoes"] = False
        elif possui_infracoes == "indisponivel":
            dados["possui_infracoes"] = None

        return RegistroInfracoes.from_dict({
            "possui_infracoes": possui_infracoes,
            "infracoes": lista_infracoes
        })

    def consulta_roubo_furto(self, placa: str):
        # 1. Pega as informações da API
        raw = self._csin.consultar_hist_roubo_furto(placa)

        # 2. Pega apenas a "infracoes_renainf" chave para tratamento
        dados: dict = _navegar_json(raw, ("dados",
                                          "historico_roubo_furto",
                                          "registros_roubo_furto"))

        if "possui_registro" not in dados:
            raise CampoAusenteErro()

        if dados.get("possui_registro") is None:
            raise CampoVazioErro()

        possui_registro = dados.get("possui_registro")

        if possui_registro not in ("sim", "nao", "indisponivel"):
            raise ValorInvalidoErro()

        if possui_registro == "sim":
            dados["possui_registro"] = True

            if "registros" not in dados:
                raise CampoAusenteErro()

            if dados.get("registros") is None:
                raise CampoVazioErro()

            registros: list[BoletimOcorrencia] = []

            for bo in dados.get("registros"):
                registros.append(BoletimOcorrencia.from_dict(bo))

        elif possui_registro == "nao":
            dados["possui_registro"] = False
        elif possui_registro == "indisponivel":
            dados["possui_registro"] = None

        return RegistroRouboFurto.from_dict({
            "possui_registro": possui_registro,
            "registros": registros
        })

    def consulta_preco_fipe(self, placa: str) -> PrecosFipe:
        # 1. Pega as informações da API
        raw = self._cfin.consultar_precos_fipe(placa)

        # 2. Pega apenas chaves para tratamento
        dvei, dtec, dcar = _checar_dados_basicos(raw)

        dados_veiculo = DadosVeiculo.from_dict(dvei)
        dados_tecnicos = DadosTecnicos.from_dict(dtec)
        dados_carga = DadosCarga.from_dict(dcar)

        veic = Veiculo.from_dict({
            "dados_veiculo": dados_veiculo,
            "dados_tecnicos": dados_tecnicos,
            "dados_carga": dados_carga
        })

        fipe = _navegar_json(raw, ("dados",))

        if "informacoes_fipe" not in fipe:
            raise CampoAusenteErro()

        info_fipe = fipe.get("informacoes_fipe")

        if info_fipe is None:
            raise CampoVazioErro()

        valores_fipe: list[InfoFipe] = []

        for i in info_fipe:
            i["preco"] = _parse_flt(i["preco"])

            valores_fipe.append(InfoFipe.from_dict(i))

        return PrecosFipe.from_dict({
            "veiculo": veic,
            "informacoes_fipe": valores_fipe
        })
