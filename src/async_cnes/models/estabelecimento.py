"""Modelos públicos para dados de estabelecimentos de saúde CNES."""

from __future__ import annotations

from pydantic import Field

from async_cnes.models.base import AsyncCnesModel


class IdentificacaoEstabelecimento(AsyncCnesModel):
    """Identificação principal do estabelecimento no CNES."""

    cnes: str | None = Field(default=None, description="Código CNES com 7 dígitos.")
    codigo_unidade: str | None = Field(default=None, description="Código interno da unidade.")
    nome_fantasia: str | None = Field(default=None, description="Nome fantasia.")
    razao_social: str | None = Field(default=None, description="Nome empresarial ou razão social.")
    cnpj: str | None = Field(default=None, description="CNPJ sem máscara.")
    data_atualizacao: str | None = Field(
        default=None,
        description="Data de atualização no formato ISO.",
    )


class Endereco(AsyncCnesModel):
    """Endereço normalizado do estabelecimento."""

    logradouro: str | None = None
    numero: str | None = None
    complemento: str | None = None
    bairro: str | None = None
    municipio: str | None = None
    codigo_municipio: str | None = None
    uf: str | None = None
    cep: str | None = None
    tipo_logradouro: str | None = None


class Contato(AsyncCnesModel):
    """Dados de contato do estabelecimento."""

    telefone: str | None = None
    telefones: list[str] = Field(default_factory=list)
    email: str | None = None


class Gestao(AsyncCnesModel):
    """Informações de gestão vinculadas ao estabelecimento."""

    municipio: str | None = None
    codigo_municipio: str | None = None
    uf: str | None = None
    esfera_administrativa: str | None = None
    codigo_esfera_administrativa: str | None = None


class NaturezaJuridica(AsyncCnesModel):
    """Natureza jurídica, preparada para contratos complementares do CNES."""

    codigo: str | None = None
    descricao: str | None = None


class AtendimentoSUS(AsyncCnesModel):
    """Indicador de atendimento ao SUS."""

    atende: bool | None = None
    descricao: str | None = None


class Localizacao(AsyncCnesModel):
    """Coordenadas do estabelecimento, quando informadas pelo CNES."""

    latitude: str | None = None
    longitude: str | None = None
    geo_json: str | None = None


class SumarioEstabelecimento(AsyncCnesModel):
    """Resumo de coleções retornadas pelo contrato SOAP."""

    quantidade_profissionais_saude: int | None = None
    quantidade_cbos: int | None = None
    quantidade_leitos: int | None = None
    quantidade_habilitacoes: int | None = None
    quantidade_equipamentos: int | None = None
    quantidade_samus: int | None = None


class EstabelecimentoSaude(AsyncCnesModel):
    """Estabelecimento de saúde normalizado e serializável."""

    cnes: str | None = None
    nome_fantasia: str | None = None
    razao_social: str | None = None
    cnpj: str | None = None
    tipo_estabelecimento: str | None = None
    codigo_tipo_estabelecimento: str | None = None
    atende_sus: bool | None = None
    telefone: str | None = None
    endereco: Endereco | None = None
    identificacao: IdentificacaoEstabelecimento | None = None
    contato: Contato | None = None
    gestao: Gestao | None = None
    natureza_juridica: NaturezaJuridica | None = None
    atendimento_sus: AtendimentoSUS | None = None
    localizacao: Localizacao | None = None
    sumario: SumarioEstabelecimento | None = None
