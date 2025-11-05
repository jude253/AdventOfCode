#!/usr/bin/env bash
set -e
# This is a simple script to make it easier for me to build project
# in the same structure repeatedly

# echo "Script name: $0"
# echo "First argument: $1"
# echo "Second argument: $2"
# echo "Total number of arguments: $#"

# Colors
GREEN="\033[0;32m"
CYAN="\033[0;36m"
NO_COLOR="\033[0m"


function install {
  echo -e "${CYAN}Installing${NO_COLOR}"
  hatch env create
  hatch run sync-venv
}

function test {
  echo -e "${GREEN}Running test${NO_COLOR}"
  hatch run check
  hatch test
}

function run {
  echo -e "${GREEN}Running 'run ${@:2}'${NO_COLOR}"
  hatch run "${@:2}"
}

function build_development {
  echo -e "${GREEN}Building for development${NO_COLOR}"
  hatch run sync-venv
  test
  hatch build
}

function build_release {
  echo -e "${GREEN}Building for release${NO_COLOR}"
  hatch run sync-venv
  test
  hatch build
}

function clean {
  echo -e "${GREEN}Running clean${NO_COLOR}"
  rm -rf dist build .venv* .*_cache **/*__pycache__
  hatch env prune
}

function print_usage {
  echo -e "${CYAN}USAGE:${NO_COLOR}"
  echo
  echo -e "    bin/build.sh [install,test,run,dev,release,clean]"
  echo
}

case "$1" in
  "install")
    install
    ;;
  "test")
    test
    ;;
  "run")
    run "$@"
    ;;
  "dev")
    build_development
    ;;
  "release")
    build_release
    ;;
  "clean")
    clean
    ;;
  *)
    print_usage
    ;;
esac
