"""Parser do contrato ConsultarEstabelecimentoSaude."""

from __future__ import annotations

from async_cnes.contracts import CONSULTAR_ESTABELECIMENTO_SAUDE
from async_cnes.exceptions import CnesNotFoundError
from async_cnes.models import (
    AtendimentoSUS,
    Contato,
    Endereco,
    EstabelecimentoSaude,
    Gestao,
    IdentificacaoEstabelecimento,
    Localizacao,
    NaturezaJuridica,
    SumarioEstabelecimento,
)
from async_cnes.parsers.soap import get_response_element
from async_cnes.parsers.xml import (
    Element,
    child_text,
    children,
    find_first,
    first_child,
    first_text,
    parse_xml,
)
from async_cnes.utils import clean_text, format_phone, parse_bool


def parse_consultar_estabelecimento_response(content: bytes | str) -> EstabelecimentoSaude:
    """Converte a resposta SOAP em um modelo público de estabelecimento."""
    root = parse_xml(content)
    response = get_response_element(root, CONSULTAR_ESTABELECIMENTO_SAUDE.response_element)
    result = first_child(response, CONSULTAR_ESTABELECIMENTO_SAUDE.result_element)
    if result is None:
        result = find_first(response, CONSULTAR_ESTABELECIMENTO_SAUDE.result_element)
    if result is None:
        msg = "CNES não retornou resultado para o estabelecimento consultado."
        raise CnesNotFoundError(msg)

    estabelecimento = first_child(result, "EstabelecimentoSaude")
    if estabelecimento is None:
        msg = "Estabelecimento de saúde não encontrado."
        raise CnesNotFoundError(msg)

    return _parse_estabelecimento(estabelecimento, first_child(result, "sumario"))


def _parse_estabelecimento(
    element: Element,
    sumario_element: Element | None,
) -> EstabelecimentoSaude:
    codigo_cnes = child_text(first_child(element, "CodigoCNES"), "codigo")
    codigo_unidade = child_text(first_child(element, "CodigoUnidade"), "codigo")
    nome_fantasia = child_text(first_child(element, "nomeFantasia"), "Nome")
    razao_social = child_text(first_child(element, "nomeEmpresarial"), "Nome")
    cnpj = child_text(first_child(element, "CNPJ"), "numeroCNPJ")
    data_atualizacao = child_text(element, "dataAtualizacao")

    tipo_unidade = first_child(element, "tipoUnidade")
    codigo_tipo = child_text(tipo_unidade, "codigo")
    tipo_estabelecimento = child_text(tipo_unidade, "descricao")

    atende_sus = parse_bool(first_text(element, ["perteceSistemaSUS", "pertenceSistemaSUS"]))
    telefones = [
        phone
        for phone in (_parse_telefone(phone) for phone in children(element, "Telefone"))
        if phone is not None
    ]
    telefone = telefones[0] if telefones else None

    identificacao = IdentificacaoEstabelecimento(
        cnes=codigo_cnes,
        codigo_unidade=codigo_unidade,
        nome_fantasia=nome_fantasia,
        razao_social=razao_social,
        cnpj=cnpj,
        data_atualizacao=data_atualizacao,
    )
    contato = _parse_contato(element, telefone, telefones)
    gestao = _parse_gestao(element)
    natureza_juridica = _parse_natureza_juridica(element)

    return EstabelecimentoSaude(
        cnes=codigo_cnes,
        nome_fantasia=nome_fantasia,
        razao_social=razao_social,
        cnpj=cnpj,
        tipo_estabelecimento=tipo_estabelecimento,
        codigo_tipo_estabelecimento=codigo_tipo,
        atende_sus=atende_sus,
        telefone=telefone,
        endereco=_parse_endereco(first_child(element, "Endereco")),
        identificacao=identificacao,
        contato=contato,
        gestao=gestao,
        natureza_juridica=natureza_juridica,
        atendimento_sus=AtendimentoSUS(
            atende=atende_sus,
            descricao=_describe_atendimento_sus(atende_sus),
        ),
        localizacao=_parse_localizacao(first_child(element, "Localizacao")),
        sumario=_parse_sumario(sumario_element),
    )


def _parse_endereco(element: Element | None) -> Endereco | None:
    if element is None:
        return None

    municipio = first_child(element, "Municipio")
    uf = first_child(municipio, "UF")
    bairro = first_child(element, "Bairro")
    cep = first_child(element, "CEP")
    tipo_logradouro = first_child(element, "TipoLogradouro")
    tipo_logradouro_desc = child_text(tipo_logradouro, "descricaoTipoLogradouro")
    nome_logradouro = child_text(element, "nomeLogradouro")

    return Endereco(
        logradouro=_compose_logradouro(tipo_logradouro_desc, nome_logradouro),
        numero=child_text(element, "numero"),
        complemento=child_text(element, "complemento"),
        bairro=child_text(bairro, "descricaoBairro") or child_text(bairro, "nomeBairro"),
        municipio=child_text(municipio, "nomeMunicipio"),
        codigo_municipio=child_text(municipio, "codigoMunicipio"),
        uf=child_text(uf, "siglaUF"),
        cep=child_text(cep, "numeroCEP"),
        tipo_logradouro=tipo_logradouro_desc,
    )


def _parse_contato(element: Element, telefone: str | None, telefones: list[str]) -> Contato | None:
    email = child_text(first_child(element, "Email"), "descricaoEmail")
    if telefone is None and not telefones and email is None:
        return None
    return Contato(telefone=telefone, telefones=telefones, email=email)


def _parse_gestao(element: Element) -> Gestao | None:
    municipio = first_child(element, "MunicipioGestor")
    esfera = first_child(element, "esferaAdministrativa")
    if municipio is None and esfera is None:
        return None

    uf = first_child(municipio, "UF")
    return Gestao(
        municipio=child_text(municipio, "nomeMunicipio"),
        codigo_municipio=child_text(municipio, "codigoMunicipio"),
        uf=child_text(uf, "siglaUF"),
        esfera_administrativa=child_text(esfera, "descricao"),
        codigo_esfera_administrativa=child_text(esfera, "codigo"),
    )


def _parse_natureza_juridica(element: Element) -> NaturezaJuridica | None:
    natureza = first_child(element, "NaturezaJuridica", "naturezaJuridica")
    if natureza is None:
        return None
    return NaturezaJuridica(
        codigo=child_text(natureza, "codigo"),
        descricao=child_text(natureza, "descricao"),
    )


def _parse_localizacao(element: Element | None) -> Localizacao | None:
    if element is None:
        return None
    return Localizacao(
        latitude=child_text(element, "latitude"),
        longitude=child_text(element, "longitude"),
        geo_json=child_text(element, "geoJson"),
    )


def _parse_sumario(element: Element | None) -> SumarioEstabelecimento | None:
    if element is None:
        return None
    return SumarioEstabelecimento(
        quantidade_profissionais_saude=_parse_int(
            child_text(element, "quantidadeProfissionaisSaude"),
        ),
        quantidade_cbos=_parse_int(child_text(element, "quantidadeCBOS")),
        quantidade_leitos=_parse_int(child_text(element, "quantidadeLeitos")),
        quantidade_habilitacoes=_parse_int(child_text(element, "quantidadeHabilitacoes")),
        quantidade_equipamentos=_parse_int(child_text(element, "quantidadeEquipamentos")),
        quantidade_samus=_parse_int(child_text(element, "quantidadeSamus")),
    )


def _parse_telefone(element: Element) -> str | None:
    return format_phone(
        ddd=child_text(element, "DDD"),
        number=child_text(element, "numeroTelefone"),
        ddi=child_text(element, "DDI"),
    )


def _compose_logradouro(tipo_logradouro: str | None, nome_logradouro: str | None) -> str | None:
    tipo = clean_text(tipo_logradouro)
    nome = clean_text(nome_logradouro)
    if tipo is None:
        return nome
    if nome is None:
        return tipo
    if nome.lower().startswith(tipo.lower()):
        return nome
    return f"{tipo.title()} {nome}"


def _parse_int(value: str | None) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except ValueError:
        return None


def _describe_atendimento_sus(value: bool | None) -> str | None:
    if value is True:
        return "Atende SUS"
    if value is False:
        return "Não atende SUS"
    return None
