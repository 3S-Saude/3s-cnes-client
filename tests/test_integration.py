import os

import pytest

from async_cnes import CnesClient


@pytest.mark.integration
@pytest.mark.skipif(
    os.getenv("ASYNC_CNES_RUN_INTEGRATION") != "1",
    reason="defina ASYNC_CNES_RUN_INTEGRATION=1 para acessar o CNES real",
)
async def test_real_consultar_estabelecimento() -> None:
    async with CnesClient() as client:
        unidade = await client.consultar_estabelecimento("2400737")

    assert unidade.cnes == "2400737"
