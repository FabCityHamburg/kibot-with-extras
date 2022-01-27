# SPDX-FileCopyrightText: 2022 Fab City Hamburg e.V.
#
# SPDX-License-Identifier: MIT

with import <nixpkgs> {};

let
  pythonEnv = python37.withPackages (ps: with ps; [
    pytest
    docker
  ]);
in mkShell {
  buildInputs = [
    pythonEnv
  ];
}
