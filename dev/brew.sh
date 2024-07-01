#!/bin/bash

SOURCE="/Users/ashishpatel/pateash/homebrew-core/Formula/h/hckr.rb"


function clean(){
  echo "Cleaning all caches"
  brew cleanup
  echo "====================================="
}

function uninstall(){
  echo "Uninstalling if exists"
  brew uninstall hckr
  echo "====================================="
}

function install(){
  echo "Installing from sources"
  brew install --verbose --build-from-source $SOURCE
  echo "====================================="
}

function test(){
  echo "Testing hckr"
  brew test hckr
  echo "====================================="
}

function audit(){
  echo "Audit hckr"
  brew audit hckr
  echo "====================================="

}

function style(){
  echo "Style hckr"
  brew style $SOURCE
  echo "====================================="
}

function tap(){
  echo "Creating a new tap with latest formulae 'hckr.rb'"
  TAP_NAME="pateash/local"
  TAP_DIR="/opt/homebrew/Library/Taps/pateash/homebrew-local/Formula/"
  # removing tap if exists
  brew untap $TAP_NAME
  echo -e "Creating tap $TAP_NAME"
  brew tap-new $TAP_NAME --no-git
  brew tap-info $TAP_NAME
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
*)
  echo -e "Invalid command, Please use $COMMANDS"
  exit 1
esac


