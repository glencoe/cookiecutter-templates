
{
  pkgs,
  lib,
  config,
  inputs,
  ...
}: {
  packages = [
    pkgs.git
    pkgs.act  # test github actions locally    
    pkgs.lazygit
    pkgs.gitu
    pkgs.git-cliff
    pkgs.asciidoctor-with-extensions
    pkgs.kramdown-asciidoc
  ];

  languages.python = {
    enable = true;
    uv.enable = true;
    uv.sync.enable = true;
    version = "{{ cookiecutter.minimum_python_version }}";
  };

  pre-commit.hooks = {
    shellcheck.enable = true;
    ruff.enable = true;
    mypy.enable = true;
    ripsecrets.enable = true;
    # vale.enable = true;
    yamlfmt.enable = true;
    actionlint.enable = true;
    alejandra.enable = true;
    check-added-large-files.enable = true;
    check-builtin-literals.enable = true;
    check-docstring-first.enable = true;
    check-json.enable = true;
    check-python.enable = true;
    check-shebang-scripts-are-executable.enable = true;
    check-symlinks.enable = true;
    check-toml.enable = true;
    check-vcs-permalinks.enable = true;
    # no-commit-to-branch.enable = true;
    # reuse.enable = true;
  };
}
