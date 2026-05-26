"""Helpers seguros para leitura de XML."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any, TypeAlias, cast

from lxml import etree

from async_cnes.exceptions import CnesValidationError
from async_cnes.utils.text import clean_text

Element: TypeAlias = Any


def parse_xml(content: bytes | str) -> Element:
    """Parseia XML com proteções contra XXE e acesso externo."""
    parser = etree.XMLParser(
        resolve_entities=False,
        no_network=True,
        load_dtd=False,
        recover=False,
        huge_tree=False,
        remove_blank_text=True,
    )
    data = content.encode("utf-8") if isinstance(content, str) else content
    try:
        return cast(Element, etree.fromstring(data, parser=parser))
    except etree.XMLSyntaxError as exc:
        msg = "Resposta XML inválida recebida do CNES."
        raise CnesValidationError(msg) from exc


def local_name(element: Element) -> str:
    """Retorna o nome local de um elemento, ignorando namespace."""
    return str(etree.QName(element).localname)


def children(element: Element, name: str | None = None) -> list[Element]:
    """Lista filhos imediatos, opcionalmente filtrando por nome local."""
    values = [child for child in element if isinstance(child.tag, str)]
    if name is None:
        return values
    return [child for child in values if local_name(child) == name]


def first_child(element: Element | None, *names: str) -> Element | None:
    """Busca o primeiro filho imediato por uma lista de nomes locais."""
    if element is None:
        return None
    for name in names:
        matches = children(element, name)
        if matches:
            return matches[0]
    return None


def find_first(element: Element | None, name: str) -> Element | None:
    """Busca em profundidade o primeiro elemento pelo nome local."""
    if element is None:
        return None
    if local_name(element) == name:
        return element
    for candidate in element.iter():
        if isinstance(candidate.tag, str) and local_name(candidate) == name:
            return candidate
    return None


def text(element: Element | None) -> str | None:
    """Extrai texto limpo de um elemento."""
    if element is None:
        return None
    return clean_text(element.text)


def child_text(element: Element | None, *path: str) -> str | None:
    """Extrai texto caminhando por filhos imediatos."""
    current = element
    for name in path:
        current = first_child(current, name)
        if current is None:
            return None
    return text(current)


def first_text(element: Element | None, names: Iterable[str]) -> str | None:
    """Extrai o texto do primeiro filho imediato encontrado."""
    if element is None:
        return None
    for name in names:
        value = child_text(element, name)
        if value is not None:
            return value
    return None
