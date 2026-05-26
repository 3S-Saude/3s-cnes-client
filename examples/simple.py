import asyncio

from async_cnes import CnesClient


async def main() -> None:
    async with CnesClient() as client:
        unidade = await client.consultar_estabelecimento("2400737")
        print(unidade)


if __name__ == "__main__":
    asyncio.run(main())
