
{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  nativeBuildInputs = with pkgs.buildPackages; [
    # System dependencies
    ncurses
    openssh
    git

    # Tools for Node environment management
    corepack_latest
    nodejs_24

    # Tools for Python environment management
    python3
    uv
  ];
}

