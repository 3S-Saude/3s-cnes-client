"""Parsing de envelopes SOAP e SOAP Fault."""

from __future__ import annotations

from typing import Any

from async_cnes.exceptions import CnesSoapFaultError, CnesValidationError
from async_cnes.parsers.xml import (
    Element,
    child_text,
    children,
    find_first,
    first_child,
    local_name,
    text,
)


def get_soap_body(root: Element) -> Element:
    """Obtém o Body do envelope SOAP."""
    body = find_first(root, "Body")
    if body is None:
        msg = "Envelope SOAP sem Body."
        raise CnesValidationError(msg)
    return body


def raise_for_soap_fault(root: Element) -> None:
    """Levanta exceção pública quando o envelope contém SOAP Fault."""
    fault = find_first(get_soap_body(root), "Fault")
    if fault is None:
        return

    fault_code = (
        child_text(first_child(fault, "Code"), "Value")
        or child_text(fault, "faultcode")
        or child_text(fault, "Code")
    )
    fault_string = (
        child_text(first_child(fault, "Reason"), "Text")
        or child_text(fault, "faultstring")
        or text(first_child(fault, "Reason"))
    )
    detail_element = first_child(fault, "Detail", "detail")
    detail = _parse_fault_detail(detail_element)
    message = fault_string or "Fault SOAP retornado pelo serviço CNES."
    raise CnesSoapFaultError(
        message,
        fault_code=fault_code,
        fault_string=fault_string,
        detail=detail,
    )


def get_response_element(root: Element, response_name: str) -> Element:
    """Retorna o elemento de resposta de uma operação SOAP."""
    raise_for_soap_fault(root)
    body = get_soap_body(root)
    response = first_child(body, response_name)
    if response is None:
        response = find_first(body, response_name)
    if response is None:
        msg = f"Resposta SOAP sem elemento {response_name!r}."
        raise CnesValidationError(msg)
    return response


def _parse_fault_detail(detail: Element | None) -> dict[str, Any]:
    if detail is None:
        return {}

    messages: list[dict[str, str | None]] = []
    for candidate in detail.iter():
        if not isinstance(candidate.tag, str) or local_name(candidate) != "Mensagem":
            continue
        messages.append(
            {
                "codigo": child_text(candidate, "codigo"),
                "descricao": child_text(candidate, "descricao"),
            }
        )

    parsed: dict[str, Any] = {
        "identificador": child_text(find_first(detail, "MSFalha"), "identificador"),
        "mensagens": messages,
    }
    if not messages and children(detail):
        parsed["raw_local_names"] = [local_name(child) for child in children(detail)]
    return parsed
