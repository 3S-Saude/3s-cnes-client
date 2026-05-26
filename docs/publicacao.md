# Publicação

Este projeto foi preparado para publicação no PyPI e no TestPyPI usando
Trusted Publishing do GitHub Actions.

## Build local

```bash
python -m pip install -e ".[dev]"
ruff check .
mypy src
pytest
python -m build
twine check dist/*
```

## TestPyPI

1. Crie o projeto `async-cnes` no TestPyPI.
2. Configure Trusted Publisher apontando para:
   - Owner/repository do GitHub;
   - workflow `.github/workflows/testpypi.yml`;
   - environment `testpypi`.
3. Execute manualmente o workflow `Publish to TestPyPI`.

## PyPI

1. Crie o projeto `async-cnes` no PyPI.
2. Configure Trusted Publisher apontando para:
   - Owner/repository do GitHub;
   - workflow `.github/workflows/pypi.yml`;
   - environment `pypi`.
3. Crie uma release no GitHub com tag semântica, por exemplo `v0.1.0`.

O workflow faz build a partir do checkout limpo e publica com OIDC, sem token
persistido no repositório.
