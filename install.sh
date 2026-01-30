#!/bin/bash


DIR="$HOME/.pvm"
ZSHRC="$HOME/.zshrc"
BASHRC="$HOME/.bashrc"
PVM_PATH_LINE='export PATH="$HOME/.pvm/bin:$PATH"'
PVM_SOURCE_LINE='source "$HOME/.pvm/sh/pvm.sh"'


function create_pvm_directory() {
  if [ ! -d "$DIR" ]; then
      echo "Creating directory: $DIR"
      mkdir -p "$DIR/versions"
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
    exit
  fi

  if ! grep -qxF "$PVM_PATH_LINE" "$RC_FILE"; then
    echo "$PVM_PATH_LINE" >> "$RC_FILE"
  fi

  if ! grep -qxF "$PVM_SOURCE_LINE" "$RC_FILE"; then
    echo "$PVM_SOURCE_LINE" >> "$RC_FILE"
  fi
}

function download_assets() {
  mkdir -p "$DIR/bin" "$DIR/sh"
  echo "Downloading assets..."

  curl -L "https://raw.githubusercontent.com/your-user/pvm/main/assets/pvm" -o "$DIR/bin/pvm"
  curl -L "https://raw.githubusercontent.com/your-user/pvm/main/assets/pvm.sh" -o "$DIR/sh/pvm.sh"
  curl -L "https://raw.githubusercontent.com/your-user/pvm/main/app/svc" -o "$DIR/bin/svc"
  curl -L "https://raw.githubusercontent.com/your-user/pvm/main/app/pvm" -o "$DIR/bin/pvm"

  chmod +x "$DIR/bin/pvm" "$DIR/sh/pvm.sh"
}


create_pvm_directory
download_assets
update_rc_file
