#!/usr/bin/env python

from subprocess import Popen, PIPE
from pathlib import Path
import os


def _run(*cmd) -> str:
    buff = []
    print("running:", " ".join(cmd))
    with Popen(cmd, stdout=PIPE, universal_newlines=True, bufsize=1) as p:
        for line in p.stdout:  # type: ignore
            print(line, end="")
            buff.append(line)
    return "\n".join(buff)


def _devenv_run(*cmd) -> str:
    return _run("devenv", "shell", "--", *cmd)


run = _run


def uv(*cmd):
    return run("uv", *cmd)


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
        p.mkdir(parents=True)


devenv_used = {%if cookiecutter.use_devenv %} True {% else %} False {% endif %}
git_cliff = {% if cookiecutter.git_cliff %} True {% else %} False {% endif %}

def uv_add(*package):
    uv("add", *package)


def add_packages(*p):
    uv_add(*p)


def add_dev_deps():
    print("INFO: adding python dev dependencies")

    ps_dev = [
        "--group",
        "dev",
        "pytest",
        "nox",
        "coverage",
        "mypy",
    ]

    if git_cliff:
        ps_dev.append("git-cliff", "opr")
    else:
        ps_dev.extend(["towncrier", "bump_my_version"])
    add_packages(*ps_dev)

    ps_lint = [
        "--group",
        "lint",
        "ruff"
    ]
    add_packages(*ps_lint)
    ps_lsp = [
        "--group",
        "lsp",
        "python-lsp-server",
        "pylsp-rope",
        "pylsp-mypy",
    ]
    add_packages(*ps_lsp)


def add_extra_dev_deps():
    add_packages("--group", "dev", "pre-commit")


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

def create_python_version_file():
    with open(".python-version", "w") as f:
        f.write("{{ cookiecutter.minimum_python_version }}")


def setup():
    global run
    create_python_version_file()
    if devenv_used:
        run = _devenv_run
    else:
        run = _run
    git_init()
    add_dev_deps()
    if not devenv_used:
        add_extra_dev_deps()
    install_packages()
    if not devenv_used:
        run_in_venv("pre-commit", "install")
        os.remove(".envrc")
    else:
        remove_precommit_config()  # devenv will manage pre-commit


if __name__ == "__main__":
    setup()
