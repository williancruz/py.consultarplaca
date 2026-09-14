# =============================================================================
# Classe Base da API :: NÍVEL 1
# =============================================================================


class ConsultarPlacaError(Exception):
    """Exceção base da biblioteca. Capture para tratar qualquer erro da API"""
    pass

# =============================================================================
# Classes de Erros :: NÍVEL 2
# =============================================================================


class ConexaoFalhouErro(Exception):
    "Sem conexão com internet ou o servidor/provedor da API está fora do ar"
    pass


class RespostaFalhouErro(Exception):
    "A conexão está OK, mas o HTTP retornou algo diferente de '200 OK'"
    pass


class RespostaInesperadaErro(ConsultarPlacaError):
    "Tudo o que não for erro de HTTP ou de rede."
    pass

# =============================================================================
# Erros de Resposta (HTTP != 200) :: NÍVEL 3
# =============================================================================


class RequisicaoInvalidaErro(RespostaFalhouErro):
    """HTTP 400 Bad Request :: Algum parâmetro está fora do padrão exigido"""
    # placa testada : AAAA0000
    # testado em 07/09/2026


class UsuarioInvalidoErro(RespostaFalhouErro):
    """HTTP 401 Unauthorized :: Usuário ou token incorreto"""
    # testado utilizando alterando uma letra do token verdadeiro
    # testado em 07/09/2026
    pass


class CreditosInsuficientesErro(RespostaFalhouErro):
    """HTTP 402 Payment Required :: Créditos insuficientes"""
    # tipo_erro=credito_insuficiente
    # testado em 07/09/2026
    pass


class RecursoBloqueadoErro(RespostaFalhouErro):
    """HTTP 403 Forbidden :: Usuário sem permissão para esse recurso/rota"""
    # Impossível testar: desconheço outras rotas além das documentadas que
    # permitem testar o bloqueio. TODO: verificar com o provedor se podem
    # me ajudar com este teste.
    pass


class RecursoInexistenteErro(RespostaFalhouErro):
    """HTTP 404 Not Found :: Recurso/rota solicitada não existe"""
    # testado em 07/09/2026 utilizando uma string aleatória
    pass


class LimiteExcedidoErro(RespostaFalhouErro):
    """HTTP 429 Too Many Requests :: >120 consultas em apenas 1 minuto"""
    # testado em 07/09/2026 utilizando loop
    pass

# =============================================================================
# Erros de Contrato da API :: NÍVEL 3
# =============================================================================


class JSONInvalidoErro(RespostaInesperadaErro):
    """Caso o retorno da API não seja um JSON ou ele esteja mal formatado"""
    pass


class CampoAusenteErro(RespostaInesperadaErro):
    """O JSON retornado é válido, mas já chaves obrigatórias ausentes"""
    pass

class CampoVazioErro(RespostaInesperadaErro):
    """Chave obrigatória existe, mas veio em branco"""
    pass


class PlacaNaoEncontradaErro(RequisicaoInvalidaErro):
    """Placa informada realmente não existe ou serviço de consulta fora do ar"""
    # tipo_erro=placa_nao_encontrada
    # erro http 400 bad request
    # placa testada : NAG-0000 (Acre)
    # testado em 08/09/2026
    pass


class ChassiNaoEncontradoErro(RequisicaoInvalidaErro):
    """Chassi informado realmente não existe ou serviço de consulta fora do ar"""
    # tipo_erro=chassi_nao_encontrado
    # erro http 400 bad request
    # chassi testado : 6FlAB5vwhc5S18631
    # testado em 08/09/2026
    pass


class InformacaoNaoEncontradaErro(RespostaInesperadaErro):
    """A placa existe, mas a API não possui informações sobre a mesma"""
    # tipo_erro=informacao_nao_encontrada
    pass


class ServicoIndisponivelErro(RespostaInesperadaErro):
    """A API não conseguiu contactar os fornecedores de informações deles"""
    # tipo_erro=servico_indisponivel
    pass

class ValorInvalidoErro(RespostaInesperadaErro):
    """Se retornar algo diferente de sim/nao/indisponivel"""
    _MSG_PADRAO = "Valor inválido recebido para {objeto!r}"

    def __init__(self, objeto: str, valor=None):
        mensagem = self._MSG_PADRAO.format(objeto=objeto)
        if valor is not None:
            mensagem += f" (valor recebido: {valor!r})"
        super().__init__(mensagem)