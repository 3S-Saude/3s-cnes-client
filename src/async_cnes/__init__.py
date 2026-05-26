"""Cliente assíncrono para o serviço SOAP oficial do CNES."""

from async_cnes.client import CnesClient
from async_cnes.exceptions import (
    CnesConnectionError,
    CnesError,
    CnesNotFoundError,
    CnesSoapFaultError,
    CnesTimeoutError,
    CnesValidationError,
)
from async_cnes.models import (
    AtendimentoSUS,
    Contato,
    Endereco,
    EstabelecimentoSaude,
    Gestao,
    IdentificacaoEstabelecimento,
    Localizacao,
    NaturezaJuridica,
    RetryConfig,
    SumarioEstabelecimento,
)

__all__ = [
    "AtendimentoSUS",
    "CnesClient",
    "CnesConnectionError",
    "CnesError",
    "CnesNotFoundError",
    "CnesSoapFaultError",
    "CnesTimeoutError",
    "CnesValidationError",
    "Contato",
    "Endereco",
    "EstabelecimentoSaude",
    "Gestao",
    "IdentificacaoEstabelecimento",
    "Localizacao",
    "NaturezaJuridica",
    "RetryConfig",
    "SumarioEstabelecimento",
]
