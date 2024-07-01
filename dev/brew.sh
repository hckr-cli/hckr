#!/bin/bash

SOURCE="/Users/ashishpatel/pateash/homebrew-core/Formula/h/hckr.rb"

#FLAGS="--debug --verbose"
FLAGS="--verbose"
function clean(){
  echo "Cleaning all caches"
  brew cleanup $FLAGS
  echo "====================================="
}

function uninstall(){
  echo "Uninstalling if exists"
  brew uninstall $FLAGS hckr
  echo "====================================="
}

function install(){
  echo "Installing from sources"
  brew install $FLAGS --build-from-source $SOURCE
  echo "====================================="
}

function test(){
  echo "Testing hckr"
  brew test $FLAGS hckr
  echo "====================================="
}

function audit(){
  echo "Audit hckr"
  brew audit --strict $FLAGS hckr
  echo "====================================="

}

function style(){
  echo "Style hckr"
  brew style $FLAGS $SOURCE
  echo "====================================="
}

function tap(){
  echo -e "Creating a new tap with latest formulae 'hckr.rb'\nAs the files are soft linked, we do not need run this again."
  TAP_NAME="pateash/local"
  TAP_DIR="/opt/homebrew/Library/Taps/pateash/homebrew-local/Formula/"
  # removing tap if exists
  brew untap $FLAGS $TAP_NAME
  echo -e "Creating tap $TAP_NAME"
  brew tap-new  $FLAGS $TAP_NAME --no-git
  brew tap-info $FLAGS $TAP_NAME
  ln -s $SOURCE $TAP_DIR # copying tap
  ls -la $TAP_DIR
  brew tap-info $TAP_NAME # checking taps after moving formulae
  echo "====================================="
}
###

CMD=$1

COMMANDS="\n==========================\ntest - Run brew test \ninstall - Install from sources\nuninstall- Uninstall hckr\nclean - Clean cache\ntap - Create tap from latest sources\naudit - Run brew audit\nstyle - Run brew style"

if [ -z $CMD ]; then
    echo -e "Please pass COMMAND, Please use $COMMANDS"
    exit 1
fi

case $CMD in
install)
  install
  ;;
uninstall)
  uninstall
  ;;
clean)
  clean
  ;;
audit)
  audit
  ;;
test)
  test
  ;;
tap)
  tap
  ;;
style)
  style
  ;;
checks) # run all checks
  test
  audit
  style
  ;;
*)
  echo -e "Invalid command, Please use $COMMANDS"
  exit 1
esac


