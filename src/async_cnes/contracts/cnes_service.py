"""Contrato SOAP do serviço oficial CnesService v1r0."""

from __future__ import annotations

from dataclasses import dataclass
from typing import cast

from lxml import etree

from async_cnes.contracts.namespaces import CNES_SERVICE_NS, CODIGO_CNES_NS, NSMAP, SOAP12_NS
from async_cnes.utils.validators import validate_cnes


@dataclass(frozen=True, slots=True)
class SoapOperation:
    """Metadados de uma operação SOAP document/literal."""

    name: str
    request_element: str
    response_element: str
    result_element: str
    soap_action: str | None = None


CONSULTAR_ESTABELECIMENTO_SAUDE = SoapOperation(
    name="consultarEstabelecimentoSaude",
    request_element="requestConsultarEstabelecimentoSaude",
    response_element="responseConsultarEstabelecimentoSaude",
    result_element="ResultadoPesquisaEstabelecimentoSaude",
    soap_action=None,
)


def build_consultar_estabelecimento_envelope(cnes: str) -> bytes:
    """Gera envelope SOAP 1.2 para consultar estabelecimento por CNES."""
    normalized_cnes = validate_cnes(cnes)
    envelope = etree.Element(etree.QName(SOAP12_NS, "Envelope"), nsmap=NSMAP)
    etree.SubElement(envelope, etree.QName(SOAP12_NS, "Header"))
    body = etree.SubElement(envelope, etree.QName(SOAP12_NS, "Body"))
    request = etree.SubElement(
        body,
        etree.QName(CNES_SERVICE_NS, CONSULTAR_ESTABELECIMENTO_SAUDE.request_element),
    )
    codigo_cnes = etree.SubElement(request, etree.QName(CODIGO_CNES_NS, "CodigoCNES"))
    codigo = etree.SubElement(codigo_cnes, etree.QName(CODIGO_CNES_NS, "codigo"))
    codigo.text = normalized_cnes
    return cast(bytes, etree.tostring(envelope, encoding="utf-8", xml_declaration=True))
