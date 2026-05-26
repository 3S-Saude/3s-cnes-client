# async-cnes

Cliente Python moderno, tipado e assíncrono para o serviço SOAP oficial do CNES
(Cadastro Nacional de Estabelecimentos de Saúde).

A biblioteca encapsula SOAP/XML e entrega modelos Pydantic serializáveis para JSON.
O usuário informa um CNES e recebe dados normalizados do estabelecimento.

## Instalação

```bash
pip install async-cnes
```

## Exemplo simples

```python
import asyncio
from async_cnes import CnesClient

async def main():
    async with CnesClient() as client:
        unidade = await client.consultar_estabelecimento("2400737")

        print(unidade)

asyncio.run(main())
```

## Exemplo JSON

```python
json_data = unidade.model_dump()

print(json_data)
```

## Exemplo JSON String

```python
json_string = unidade.model_dump_json(indent=2)

print(json_string)
```

## Tratamento de erros

```python
import asyncio

from async_cnes import CnesClient
from async_cnes.exceptions import (
    CnesConnectionError,
    CnesNotFoundError,
    CnesSoapFaultError,
    CnesTimeoutError,
    CnesValidationError,
)

async def main():
    try:
        async with CnesClient(timeout=15.0) as client:
            unidade = await client.consultar_estabelecimento("2400737")
            print(unidade.model_dump())
    except CnesValidationError:
        print("CNES inválido")
    except CnesNotFoundError:
        print("Estabelecimento não encontrado")
    except CnesSoapFaultError as exc:
        print(exc.fault_string)
    except CnesTimeoutError:
        print("Timeout ao consultar o CNES")
    except CnesConnectionError:
        print("Falha de conexão com o CNES")

asyncio.run(main())
```

## Configuração

```python
from async_cnes import CnesClient, RetryConfig

client = CnesClient(
    endpoint="https://servicos.saude.gov.br/cnes/CnesService/v1r0",
    timeout=10.0,
    retry=RetryConfig(enabled=True, max_attempts=3, initial_backoff=0.2, max_backoff=2.0),
    headers={"X-Request-Id": "exemplo"},
    user_agent="minha-aplicacao/1.0",
    proxy=None,
)
```

## Contrato SOAP implementado

WSDL oficial:

```text
https://servicos.saude.gov.br/cnes/CnesService/v1r0?wsdl
```

Primeira operação implementada:

```text
consultarEstabelecimentoSaude
```

O contrato usa SOAP 1.2 document/literal. O `soapAction` não é obrigatório.
A requisição envia `requestConsultarEstabelecimentoSaude` com
`CodigoCNES/codigo`, validado como string de 7 dígitos.

## Desenvolvimento

```bash
python -m pip install -e ".[dev]"
ruff check .
mypy src
pytest
python -m build
```

Os testes unitários usam respostas SOAP mockadas e não acessam o serviço real.
Testes de integração são opcionais:

```bash
ASYNC_CNES_RUN_INTEGRATION=1 pytest -m integration
```

## Publicação

O projeto inclui workflows de GitHub Actions para lint, type checking, testes,
build, TestPyPI e PyPI com Trusted Publishing. Veja `docs/publicacao.md`.
