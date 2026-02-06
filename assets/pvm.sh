WHITE='\033[0m'
RED='\033[0;31m'

# Capture original PATH once per shell
if [[ -z "${__PVM_ORIGINAL_PATH+x}" ]]; then
  __PVM_ORIGINAL_PATH="$PATH"
fi

pvm() {
  if [[ "$1" == "use" || "$1" == "deactivate" ]]; then
    eval "$(command pvm "$@")"
  else
    command pvm "$@"
  fi
}

__PVM_LAST_VERSION=""
__PVM_WARNED_VERSION=""
__PVM_ACTIVE_VENV=""

__pvm_restore_path() {
  __pvm_strip_path
  export PATH
}

__pvm_read_global_version() {
  local file="$HOME/.pvm/bin/global-version"
  [[ -f "$file" ]] || return 1
  __pvm_read_version "$file"
}

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

__pvm_strip_path() {
  local new_path=""
  local part
  local IFS=':'

  for part in $PATH; do
    if [[ "$part" == "$HOME/.pvm/versions/python-"*/python/bin ]]; then
      continue
    fi
    new_path="${new_path:+$new_path:}$part"
  done

  PATH="$new_path"
}

__pvm_read_version() {
  sed -e 's/#.*//' \
      -e 's/^[[:space:]]*//' \
      -e 's/[[:space:]]*$//' \
      "$1"
}

__pvm_resolve_version() {
  local required="$1"
  local base="$HOME/.pvm/versions"
  local best=""

  setopt localoptions nullglob 2>/dev/null

  for d in "$base"/python-*; do
    [[ -d "$d" ]] || continue
    local v="${d##*/python-}"

    if __pvm_version_matches "$required" "$v"; then
      best="$(printf '%s\n%s\n' "$best" "$v" | sort -V | tail -n1)"
    fi
  done

  [[ -n "$best" ]] && echo "$best"
}

__pvm_prepend_version() {
  __pvm_strip_path
  PATH="$1/python/bin:$PATH"
  export PATH
}

__pvm_version_matches() {
  [[ "$2" == "$1" || "$2" == "$1".* ]]
}

__pvm_find_venv() {
  for name in .venv venv; do
    if [[ -f "$PWD/$name/bin/activate" ]]; then
      echo "$PWD/$name"
      return 0
    fi
  done
  return 1
}

__pvm_activate_venv() {
  local venv="$1"

  [[ "$VIRTUAL_ENV" == "$venv" ]] && return

  if type deactivate >/dev/null 2>&1; then
    deactivate
  fi

  # shellcheck disable=SC1090
  source "$venv/bin/activate"
}

__pvm_deactivate_venv() {
  if type deactivate >/dev/null 2>&1; then
    deactivate
  fi
}

__pvm_hook() {
  local version_file version resolved global_version venv

  # ---- Local virtualenv (highest priority) ----
  if venv="$(__pvm_find_venv)"; then
    if [[ "$__PVM_ACTIVE_VENV" != "$venv" ]]; then
      __pvm_activate_venv "$venv"
      __PVM_ACTIVE_VENV="$venv"
    fi
    __PVM_LAST_VERSION="venv:$venv"
    __PVM_WARNED_VERSION=""
    return
  fi

  # Deactivate venv when leaving venv project
  if [[ -n "$__PVM_ACTIVE_VENV" ]]; then
    __pvm_deactivate_venv
    __PVM_ACTIVE_VENV=""
  fi

  # ---- Project-local version ----
  if version_file="$(__pvm_find_version_file)"; then
    version="$(__pvm_read_version "$version_file")"

    if [[ "$version" != "$__PVM_LAST_VERSION" ]]; then
      resolved="$(__pvm_resolve_version "$version")"

      if [[ -n "$resolved" ]]; then
        __pvm_prepend_version "$HOME/.pvm/versions/python-$resolved"
        __PVM_WARNED_VERSION=""
      else
        __pvm_restore_path
        if [[ "$__PVM_WARNED_VERSION" != "$version" ]]; then
          echo -e "${RED}pvm: warning: python version '$version' is required but not installed${WHITE}" >&2
          __PVM_WARNED_VERSION="$version"
        fi
      fi

      __PVM_LAST_VERSION="$version"
    fi
    return
  fi

  # ---- Global fallback ----
  if global_version="$(__pvm_read_global_version)"; then
    if [[ "global:$global_version" != "$__PVM_LAST_VERSION" ]]; then
      resolved="$(__pvm_resolve_version "$global_version")"
      [[ -n "$resolved" ]] && __pvm_prepend_version "$HOME/.pvm/versions/python-$resolved" || __pvm_restore_path
      __PVM_LAST_VERSION="global:$global_version"
      __PVM_WARNED_VERSION=""
    fi
    return
  fi

  # ---- System fallback ----
  __pvm_restore_path
  __PVM_LAST_VERSION=""
  __PVM_WARNED_VERSION=""
}

if [[ -n "$BASH_VERSION" ]]; then
  PROMPT_COMMAND="__pvm_hook${PROMPT_COMMAND:+;$PROMPT_COMMAND}"
fi

if [[ -n "$ZSH_VERSION" ]]; then
  autoload -Uz add-zsh-hook
  add-zsh-hook chpwd __pvm_hook
  add-zsh-hook precmd __pvm_hook
fi