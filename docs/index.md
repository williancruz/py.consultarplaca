# Introdução


# Consultas Disponíveis
| Consulta | Consulta Avulsa? | Opção no Relatório |
| :--- | :---: | :---: |
| **Informações gerais** (Chassi, N° Motor, Marca, Modelo e Ano) | ✔ | 8 |
| **Verificação junto a Base Estadual** como **Renavam** e Restrições | ✔ <sup>(1)</sup> | 7 |
| **Verificação junto ao Registro Nacional** de Infrações de Trânsito (RENAINF) | ✔ | 17 |
| **Histórico de Roubo e Furto** | ✔ | 4 |
| **Registro de Ofertas em Leilões Prime (Com Classificação)** | ✔ | 3 |
| **Registro de Remarketing / Desmobilização de Frota** | ✔ | 3 |
| Registro de Ofertas em **Leilões Simples** (NÃO verifica Leilões Corporativo, Privado e Varejo) <sup>2</sup> | ✘ | ✘ |
| **Informações sobre a ocorrência** de sinistros com Perda Total (PT) | ✔ | 1 |
| **Verificação junto a Base Federal** sobre Restrições Financeiras e Judiciais (RENAJUD) | ✘ | 5 |
| **GRAVAME** (Alienação Fiduciária) | ✔ | 10 |
| **Referência de Preço (Fipe)** | ✔ | 27 |
| **Histórico Recall** | ✘ | 18 |
| **Guia de Imagens** | ✘ | 19 |
| **Ficha Técnica Comparativa** | ✘ | 23 |
| **Custo Médio de Manutenção** | ✘ | 24 |
| **Proprietário atual do veículo** (Exibe apenas o primeiro nome e os dígitos iniciais do documento, sem identificar a pessoa) | ✔ | 25 |
| **Emissão de CRLV-e** (Certificado de Registro e Licenciamento de Veículo) <sup>2</sup> | ✘ | ✘ |
| **Emissão de CSV** Certificado de Segurança Veicular (Registros posteriores a 2016) <sup>2</sup>  | ✘ | ✘ |

<sup>1</sup> Apenas número do RENAVAM  
<sup>2</sup> Disponível apenas no Relatório Web

# Arquitetura
1. **Camada de Transporte / Cliente HTTP Base (```http_client.py```)**  
    Essa camada não sabe nada sobre as regras de negócio da API, apenas sobre o protocolo HTTP.  

    Responsabilidade:  
    * Gerenciar a sessão HTTP (timeouts, conexões persistentes, headers padrão, autenticação).
    * Executar verbos básicos (GET, POST, etc.).
    * Lançar erros caso ocorra falha de rede ou códigos HTTP 4xx/5xx.

    Isolamento: Nenhum modelo de dados é processado aqui; ela apenas devolve a resposta crua (dicionário parseado de JSON ou o próprio objeto de resposta).

2. **Camada de Recursos / Endpoints (```resources/*```)**  
    Como a API tem várias rotas e tipos de consultas, agrupá-las por domínio evita um arquivo cliente gigantesco.

    Responsabilidade: 
    * Conhecer os detalhes de rotas específicas.

    Fluxo interno do método:
    1. Monta os parâmetros/payload específicos daquela consulta.
    2. Dispara a chamada através do cliente HTTP.
    3. Passa o resultado pelo validador de resposta.
    4. Envia os dados limpos para a camada de Modelagem.
    5. Retorna o Objeto Padronizado pronto para quem chamou.