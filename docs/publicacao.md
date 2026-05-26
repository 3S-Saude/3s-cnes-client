# Publicação

Este projeto foi preparado para publicação no PyPI usando Trusted Publishing
do GitHub Actions, seguindo o mesmo padrão do `3s-cadsus-client`.

## Build local

```bash
python -m pip install -e ".[dev]"
ruff check .
mypy src
pytest
python -m build
twine check dist/*
```

## PyPI

1. Crie o projeto `3s-cnes-client` no PyPI.
2. Configure Trusted Publisher apontando para:
   - Owner: `3S-Saude`;
   - Repository name: `3s-cnes-client`;
   - workflow `.github/workflows/publish.yml`;
   - environment `pypi`.
3. Abra um pull request para `main`.
4. Ao fazer merge do pull request, o workflow gera os artefatos e publica no PyPI.

O workflow faz build a partir do checkout limpo e publica com OIDC, sem token
persistido no repositório.
