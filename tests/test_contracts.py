from lxml import etree

from async_cnes.contracts import build_consultar_estabelecimento_envelope
from async_cnes.exceptions import CnesValidationError


def test_build_consultar_estabelecimento_envelope() -> None:
    envelope = build_consultar_estabelecimento_envelope("2400737")
    root = etree.fromstring(envelope)

    assert etree.QName(root).localname == "Envelope"
    assert root.xpath("//*[local-name()='requestConsultarEstabelecimentoSaude']")
    codigo = root.xpath("//*[local-name()='CodigoCNES']/*[local-name()='codigo']/text()")
    assert codigo == ["2400737"]


def test_build_envelope_validates_cnes() -> None:
    try:
        build_consultar_estabelecimento_envelope("123")
    except CnesValidationError as exc:
        assert "7 dígitos" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("CnesValidationError não foi levantado")
