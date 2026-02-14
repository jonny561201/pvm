#!/bin/bash


DIR="$HOME/.pvm"
ZSHRC="$HOME/.zshrc"
BASHRC="$HOME/.bashrc"
PVM_PATH_LINE='export PATH="$HOME/.pvm/bin:$HOME/.pvm/python:$PATH"'
PVM_SOURCE_LINE='source "$HOME/.pvm/sh/pvm.sh"'


function create_pvm_directory() {
  if [ ! -d "$DIR" ]; then
      echo "Creating directory: $DIR"
      mkdir -p "$DIR/versions"
      mkdir -p "$DIR/bin"
      mkdir -p "$DIR/sh"
      mkdir -p "$DIR/python"
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
  unzip -q "$TMP_ZIP" -d "$DIR"
  rm "$TMP_ZIP"
}

function validate_extraction() {
  if [ ! -d "$DIR/pvm-main/svc" -o ! -d "$DIR/pvm-main/assets" ]; then
    echo "Error: Failed to unzip the installation zip from github!"
    echo "Contents of $DIR:"
    ls -R "$DIR"
    exit 1
  fi
}


function copy_pvm_assets() {
  cp -r "$DIR/pvm-main/svc" "$DIR/bin/"
  cp "$DIR/pvm-main/app.py" "$DIR/bin/"
  cp "$DIR/pvm-main/assets/pvm" "$DIR/bin/"
  cp "$DIR/pvm-main/assets/pvm.sh" "$DIR/sh/"

  rm -rf "$DIR/pvm-main"
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
validate_extraction
copy_pvm_assets
update_rc_file
success_message
