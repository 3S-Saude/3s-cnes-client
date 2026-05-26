import json

import pytest

from async_cnes.exceptions import CnesNotFoundError, CnesSoapFaultError
from async_cnes.parsers import parse_consultar_estabelecimento_response

from .fixtures import SOAP_EMPTY_RESPONSE, SOAP_FAULT_RESPONSE, SOAP_SUCCESS_RESPONSE


def test_parse_consultar_estabelecimento_response() -> None:
    unidade = parse_consultar_estabelecimento_response(SOAP_SUCCESS_RESPONSE)

    assert unidade.cnes == "2400737"
    assert unidade.nome_fantasia == "Hospital Exemplo"
    assert unidade.razao_social == "Hospital Exemplo LTDA"
    assert unidade.cnpj == "00000000000000"
    assert unidade.tipo_estabelecimento == "Hospital Geral"
    assert unidade.atende_sus is True
    assert unidade.telefone == "(84) 4000-0000"
    assert unidade.endereco is not None
    assert unidade.endereco.logradouro == "Rua Exemplo"
    assert unidade.endereco.bairro == "Centro"
    assert unidade.endereco.municipio == "Natal"
    assert unidade.endereco.uf == "RN"
    assert unidade.endereco.cep == "59000000"
    assert unidade.contato is not None
    assert unidade.contato.email == "contato@example.org"
    assert unidade.gestao is not None
    assert unidade.gestao.esfera_administrativa == "Municipal"
    assert unidade.sumario is not None
    assert unidade.sumario.quantidade_equipamentos == 5


def test_parse_response_is_json_serializable() -> None:
    unidade = parse_consultar_estabelecimento_response(SOAP_SUCCESS_RESPONSE)
    payload = unidade.model_dump()

    assert payload["cnes"] == "2400737"
    assert payload["identificacao"]["data_atualizacao"] == "2026-05-26"
    json.dumps(payload)
    assert '"cnes":"2400737"' in unidade.model_dump_json()


def test_parse_empty_response_raises_not_found() -> None:
    with pytest.raises(CnesNotFoundError):
        parse_consultar_estabelecimento_response(SOAP_EMPTY_RESPONSE)


def test_parse_soap_fault() -> None:
    with pytest.raises(CnesSoapFaultError) as exc_info:
        parse_consultar_estabelecimento_response(SOAP_FAULT_RESPONSE)

    exc = exc_info.value
    assert exc.fault_code == "soap:Sender"
    assert exc.detail["identificador"] == "abc-123"
    assert exc.detail["mensagens"][0]["codigo"] == "CNES-001"
