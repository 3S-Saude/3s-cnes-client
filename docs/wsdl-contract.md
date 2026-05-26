# Contrato CNES v1r0

Inspeção realizada contra o WSDL oficial:

```text
https://servicos.saude.gov.br/cnes/CnesService/v1r0?wsdl
```

## Serviço

- Nome: `CnesService`
- Endpoint real: `https://servicos.saude.gov.br/cnes/CnesService/v1r0`
- Binding: SOAP 1.2
- Estilo: `document`
- Uso: `literal`
- SOAP Action: não obrigatório (`soapActionRequired="false"`)
- Namespace do serviço: `http://servicos.saude.gov.br/cnes/v1r0/cnesservice`

## Operações disponíveis

- `consultarEstabelecimentoSaude`
- `consultarEstabelecimentoSaudePorMunicipio`
- `consultarDadosComplementaresEstabelecimentoSaude`

## Operação implementada

### `consultarEstabelecimentoSaude`

Documentação do WSDL: consultar o estabelecimento de saúde pelo código CNES.

Request:

- Elemento: `requestConsultarEstabelecimentoSaude`
- Namespace: `http://servicos.saude.gov.br/cnes/v1r0/cnesservice`
- Campo obrigatório: `CodigoCNES`
- Namespace de `CodigoCNES`: `http://servicos.saude.gov.br/schema/cnes/v1r0/codigocnes`
- Estrutura: `CodigoCNES/codigo`
- Restrição de `codigo`: string com exatamente 7 dígitos, padrão `[0-9]*`

Response:

- Elemento: `responseConsultarEstabelecimentoSaude`
- Campo opcional: `ResultadoPesquisaEstabelecimentoSaude`
- Namespace: `http://servicos.saude.gov.br/wsdl/mensageria/v1r0/resultadopesquisaestabelecimentosaude`

Estrutura principal de `ResultadoPesquisaEstabelecimentoSaude`:

- `EstabelecimentoSaude` opcional, tipo `DadosGeraisEstabelecimentoSaudeType`
- `profissional` zero ou muitos
- `leito` zero ou muitos
- `habilitacao` zero ou muitos
- `equipamento` zero ou muitos
- `samu` zero ou muitos
- `sumario` obrigatório

Campos mapeados inicialmente em `DadosGeraisEstabelecimentoSaudeType`:

- `CodigoCNES/codigo`
- `CodigoUnidade/codigo`
- `nomeFantasia/Nome`
- `nomeEmpresarial/Nome`
- `CNPJ/numeroCNPJ`
- `Endereco`
- `dataAtualizacao`
- `tipoUnidade/codigo`
- `tipoUnidade/descricao`
- `esferaAdministrativa/codigo`
- `esferaAdministrativa/descricao`
- `MunicipioGestor`
- `Telefone`
- `Email/descricaoEmail`
- `Localizacao`
- `perteceSistemaSUS`

Observação: o contrato oficial contém o campo escrito como
`perteceSistemaSUS`. A biblioteca também tolera `pertenceSistemaSUS` para
compatibilidade defensiva.

## SOAP Fault

O WSDL declara `CnesFault` com elemento `MSFalha`, no namespace:

```text
http://servicos.saude.gov.br/wsdl/mensageria/falha/v5r0/msfalha
```

Estrutura:

- `identificador` opcional
- `Mensagem` zero ou muitas
- `Mensagem/codigo`
- `Mensagem/descricao`

A biblioteca converte faults para `CnesSoapFaultError` e preserva os detalhes
em um `dict` JSON serializável.
