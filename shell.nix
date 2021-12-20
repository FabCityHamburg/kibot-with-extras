with import <nixpkgs> {};

let
  pythonEnv = python37.withPackages (ps: with ps; [
    pytest
    docker
   # pytest-bdd
  ]);
in mkShell {
  buildInputs = [
    pythonEnv
  ];
}
