import asyncio

from async_cnes import CnesClient
from async_cnes.exceptions import (
    CnesConnectionError,
    CnesNotFoundError,
    CnesSoapFaultError,
    CnesTimeoutError,
    CnesValidationError,
)


async def main() -> None:
    try:
        async with CnesClient(timeout=15.0) as client:
            unidade = await client.consultar_estabelecimento("2400737")
    except CnesValidationError:
        print("CNES inválido.")
    except CnesNotFoundError:
        print("Estabelecimento não encontrado.")
    except CnesSoapFaultError as exc:
        print(f"SOAP Fault: {exc.fault_string}")
    except CnesTimeoutError:
        print("Timeout ao consultar o CNES.")
    except CnesConnectionError:
        print("Falha de conexão com o CNES.")
    else:
        print(unidade.model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(main())
