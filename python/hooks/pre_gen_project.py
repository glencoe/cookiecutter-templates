#!/usr/bin/env python

from subprocess import run as _srun
from sys import exit


def run(*cmd) -> str:
    return _srun(cmd, check=True, text=True, capture_output=True).stdout


def uv_is_installed() -> bool:
    try:
        run("uv", "--version")
        return True
    except Exception:
        return False


if __name__ == "__main__":
    if not uv_is_installed():
        print("ERROR: uv is not installed!")
        exit(1)
