pvm() {
  if [ "$1" = "use" ] || [ "$1" = "deactivate" ]; then
    eval "$(command pvm "$@")"
  else
    command pvm "$@"
  fi
}

__PVM_LAST_PWD=""
__PVM_LAST_VERSION=""


__pvm_find_version_file() {
  local dir="$PWD"
  while [[ "$dir" != "/" ]]; do
    if [[ -f "$dir/.python-version" ]]; then
      echo "$dir/.python-version"
      return 0
    fi
    dir="${dir%/*}"
    [[ -z "$dir" ]] && dir="/"
  done
  return 1
}

__pvm_hook() {
  [[ "$PWD" == "$__PVM_LAST_PWD" ]] && return 0
  __PVM_LAST_PWD="$PWD"

  local version_file
  version_file="$(__pvm_find_version_file)" || {
    __PVM_LAST_VERSION=""
    return 0
  }

  local version
  version="$(<"$version_file")"
  version="${version## }"
  version="${version%% }"
  [[ -z "$version" ]] && return 0

  [[ "$version" == "$__PVM_LAST_VERSION" ]] && return 0

  if [[ -d "$HOME/.pvm/versions/python-$version" ]]; then
    ln -sfn "$HOME/.pvm/versions/python-$version" "$HOME/.pvm/current"
    __PVM_LAST_VERSION="$version"
  fi
}

if [[ -n "$BASH_VERSION" ]]; then
  PROMPT_COMMAND="__pvm_hook${PROMPT_COMMAND:+;$PROMPT_COMMAND}"
fi

#just a pvm wrapper to exec print commands