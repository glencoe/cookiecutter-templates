from subprocess import run as _srun
from pathlib import Path
import os


def run(*cmd) -> str:
    return _srun(cmd, check=True, text=True, capture_output=True).stdout


def uv(*cmd):
    return run("uv", "--no-progress", *cmd)


def create_project_directories():
    production_code_dir = Path("src/{{ cookiecutter.project_slug }}")
    testing_dir = Path("testing/{{ cookiecutter.project_slug }}")
    for p in [
        (testing_dir / "unit"),
        (testing_dir / "integration"),
        (testing_dir / "system"),
        production_code_dir,
        Path("docs"),
    ]:
        p.mkdir()


devenv_used = (
    True if "{% if cookiecutter.use_devenv }using{%endif}" == "using" else False
)


def uv_add(package):
    uv("add", package)


def add_package(p):
    uv_add(p)


def add_dev_deps():
    print("INFO: adding python dev dependencies")

    packages = [
        "pytest",
        "nox",
        "coverage",
        "git-cliff",
        "ruff",
        "mypy",
        "python-lsp-server",
        "pylsp-rope",
        "pylsp-mypy",
    ]

    for p in packages:
        add_package(p)


def add_extra_dev_deps():
    packages = [
        "pre-commit",
    ]

    for p in packages:
        add_package(p)


def install_packages():
    print("INFO: installing packages into venv, this will take some time.")
    uv_sync()


def uv_sync():
    uv("sync")


def uv_run(*args):
    return uv("run", *args)


def git_init():
    run("git", "init")
    run("git", "remote", "add", "origin", "{{ cookiecutter.git_repository }}")


def remove_precommit_config():
    os.remove(".pre-commit-config.yaml")


def run_in_venv(*args):
    return uv_run(*args)


def setup():
    create_project_directories()
    git_init()
    add_dev_deps()
    if not devenv_used:
        add_extra_dev_deps()
    install_packages()
    if not devenv_used:
        run_in_venv("pre-commit", "install")
    else:
        remove_precommit_config()  # devenv will manage pre-commit


if __name__ == "__main__":
    setup()
