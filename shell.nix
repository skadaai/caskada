{ pkgs ? import <nixpkgs> {} }:

let
  venvDir = "./.venv";
in pkgs.mkShell {
  nativeBuildInputs = with pkgs.buildPackages; [
    ncurses
    openssh
    git
    corepack_24
    nodejs-slim
    uv
  ];

  packages = [
    (pkgs.python3.withPackages (python-pkgs: [
      python-pkgs.pytest
      python-pkgs.pytest-asyncio
    ]))
  ];
}
