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
