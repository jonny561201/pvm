# Capture original PATH once per shell
if [[ -z "${__PVM_ORIGINAL_PATH+x}" ]]; then
  __PVM_ORIGINAL_PATH="$PATH"
fi

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

  local version_file version version_dir

  version_file="$(__pvm_find_version_file)" || {
    # No version file found → restore original PATH
    [[ -n "$__PVM_LAST_VERSION" ]] && __pvm_restore_path
    __PVM_LAST_VERSION=""
    __PVM_ACTIVE_VERSION=""
    return 0
  }

  version="$(__pvm_read_version "$version_file")"
  [[ -z "$version" ]] && return 0

  # Fast path: version unchanged
  [[ "$version" == "$__PVM_LAST_VERSION" ]] && return 0

  resolved="$(__pvm_resolve_version "$version")"

  if [[ "$resolved" == "$__PVM_ACTIVE_VERSION" ]]; then
    __PVM_LAST_VERSION="$version"
    return 0
  fi

  if [[ -n "$resolved" ]]; then
    __pvm_prepend_version "$HOME/.pvm/versions/python-$resolved"
    __PVM_LAST_VERSION="$version"
    __PVM_ACTIVE_VERSION="$resolved"
  else
    # No compatible version installed
    __pvm_restore_path
    __PVM_LAST_VERSION="$version"
    __PVM_ACTIVE_VERSION=""
  fi
}

if [[ -n "$BASH_VERSION" ]]; then
  PROMPT_COMMAND="__pvm_hook${PROMPT_COMMAND:+;$PROMPT_COMMAND}"
fi

if [[ -n "$ZSH_VERSION" ]]; then
  autoload -Uz add-zsh-hook
  add-zsh-hook chpwd __pvm_hook
  __pvm_hook
fi


__pvm_strip_path() {
  local new_path=""
  local part

  IFS=':' read -r -a parts <<< "$PATH"
  for part in "${parts[@]}"; do
    if [[ "$part" == "$HOME/.pvm/versions/python-"*/bin ]]; then
      continue
    fi
    new_path="${new_path:+$new_path:}$part"
  done

  PATH="$new_path"
}


__pvm_resolve_version() {
  local required="$1"
  local base="$HOME/.pvm/versions"
  local best=""

  for d in "$base"/python-*; do
    [[ -d "$d" ]] || continue
    local v="${d##*/python-}"

    if __pvm_version_matches "$required" "$v"; then
      if [[ -z "$best" || "$v" > "$best" ]]; then
        best="$v"
      fi
    fi
  done

  [[ -n "$best" ]] && echo "$best"
}


__pvm_read_version() {
  sed -e 's/#.*//' \
      -e 's/^[[:space:]]*//' \
      -e 's/[[:space:]]*$//' \
      "$1"
}


__pvm_prepend_version() {
  local version_dir="$1"

  __pvm_strip_path
  PATH="$version_dir/bin:$PATH"
  export PATH
}


__pvm_restore_path() {
  __pvm_strip_path
  export PATH
}


__pvm_version_matches() {
  local required="$1"
  local active="$2"

  IFS='.' read -r -a req <<< "$required"
  IFS='.' read -r -a act <<< "$active"

  local i
  for ((i=0; i<${#req[@]}; i++)); do
    [[ "${req[i]}" != "${act[i]}" ]] && return 1
  done
  return 0
}

#just a pvm wrapper to exec print commands