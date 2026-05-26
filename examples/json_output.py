import asyncio

from async_cnes import CnesClient


async def main() -> None:
    async with CnesClient() as client:
        unidade = await client.consultar_estabelecimento("2400737")

    print(unidade.model_dump())
    print(unidade.model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(main())
