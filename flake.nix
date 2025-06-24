{
  description = "Depth Eye Project";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
        };

        numpyDeps = with pkgs; [
          blas
          lapack
          libffi
          stdenv.cc.cc
          gcc.cc.lib
        ];

        # If you need Python support in Neovim
        pythonForNeovim = pkgs.python3.withPackages (ps: with ps; [
          pynvim
        ]);
        venvDir = "./venv";
      in {
        devShells.default = pkgs.mkShell {
          buildInputs = [
            pkgs.python313
            pkgs.python313Packages.pip
            pkgs.neovim
            pkgs.tree
            pkgs.git
            pkgs.cmake
            pythonForNeovim
          ] ++ numpyDeps;

          shellHook = ''
            echo "Neovim available. Using config from: $HOME/.config/nvim"
            if [ ! -d "${venvDir}" ]; then
                python -m venv ${venvDir}
              fi
              source ${venvDir}/bin/activate
            export EDITOR=nvim
            export LD_LIBRARY_PATH=${pkgs.gcc.cc.lib}/lib:$LD_LIBRARY_PATH
          '';
        };
      });
}
