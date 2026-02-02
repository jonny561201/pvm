#!/bin/bash


DIR="$HOME/.pvm"
ZSHRC="$HOME/.zshrc"
BASHRC="$HOME/.bashrc"
PVM_PATH_LINE='export PATH="$HOME/.pvm/bin:$PATH"'
PVM_SOURCE_LINE='source "$HOME/.pvm/sh/pvm.sh"'
#GITHUB_URL="https://raw.githubusercontent.com/jonny561201/pvm/main"


function create_pvm_directory() {
  if [ ! -d "$DIR" ]; then
      echo "Creating directory: $DIR"
      mkdir -p "$DIR/versions"
      mkdir -p "$DIR/bin"
      mkdir -p "$DIR/sh"
  else
      echo "Directory already exists: $DIR"
  fi
}


function update_rc_file() {
  if [ -f "$ZSHRC" ]; then
      RC_FILE="$ZSHRC"
  elif [ -f "$BASHRC" ]; then
      RC_FILE="$BASHRC"
  else
    echo "Warning: no shell rc file found; create one and add:"
    echo 'export PATH="$HOME/.pvm/bin:$PATH"'
    echo 'source "$HOME/.pvm/sh/pvm.sh"'
    exit 1
  fi

  if ! grep -qxF "$PVM_PATH_LINE" "$RC_FILE"; then
    echo "$PVM_PATH_LINE" >> "$RC_FILE"
  fi

  if ! grep -qxF "$PVM_SOURCE_LINE" "$RC_FILE"; then
    echo "$PVM_SOURCE_LINE" >> "$RC_FILE"
  fi
}


function download_extract_assets() {
  TMP_ZIP="/tmp/pvm-main.zip"
  curl -L "https://github.com/jonny561201/pvm/archive/refs/heads/main.zip" -o "$TMP_ZIP"
  unzip "$TMP_ZIP" "pvm-main/*" -d "$DIR"
  rm "$TMP_ZIP"

  cp -r "$DIR/pvm-main/svc" "$DIR/bin/"
  cp "$DIR/pvm-main/app.py" "$DIR/bin/"
  cp "$DIR/pvm-main/assets/pvm" "$DIR/bin/"
  cp "$DIR/pvm-main/assets/pvm.sh" "$DIR/sh/"

  rm -rf "$DIR/pvm-main"


#  mkdir -p "$DIR/bin" "$DIR/sh"
#  echo "Downloading assets..."
#
#  curl -L "$GITHUB_URL/assets/pvm" -o "$DIR/bin/pvm"
#  curl -L "$GITHUB_URL/svc" -o "$DIR/bin/svc/"
#  curl -L "$GITHUB_URL/assets/pvm.sh" -o "$DIR/sh/pvm.sh"
#  curl -L "$GITHUB_URL/pvm" -o "$DIR/bin/pvm"

  chmod +x "$DIR/bin/pvm" "$DIR/sh/pvm.sh"
}


function success_message() {
  echo "---------------------------------------"
  echo "pvm installed."
  echo "Run: source $RC_FILE"
  echo "or open a new terminal."
}


create_pvm_directory
download_extract_assets
#update_rc_file
#success_message
