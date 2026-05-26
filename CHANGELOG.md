# Changelog

Todas as mudanças relevantes deste projeto serão documentadas aqui.

O formato segue a ideia de Keep a Changelog e versionamento semântico.

## [0.1.0] - 2026-05-26

### Adicionado

- Cliente público assíncrono `CnesClient`.
- Operação `consultar_estabelecimento`.
- Transporte HTTP com `httpx.AsyncClient`.
- Retry opcional com exponential backoff.
- Parsing seguro de XML com `lxml`.
- Tratamento de SOAP Fault.
- Modelos Pydantic serializáveis para JSON.
- Testes unitários com respostas SOAP mockadas.
- Workflow de build, validação e publicação no PyPI com Trusted Publishing.
