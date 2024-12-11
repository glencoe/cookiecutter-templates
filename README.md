# cookiecutter templates for easy project setup

## python

Use `uv`, `ruff` and optionally `devenv`.
Run
```bash
$ cookiecutter https://github.com/glencoe/cookiecutter-templates --directory=python
```

The post project generation hooks will take care of 

- adding and installing dev deps
  - pytest
  - coverage
  - mypy
  - pre-commit
  - python-lsp-server
  - nox
- initializing the git repo
- adding the remote git repo as origin


If you have `devenv` and `cachix` installed you can choose to use devenv for maintaining
non-python deps.
