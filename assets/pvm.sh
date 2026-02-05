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

  # Split PATH safely in both bash and zsh
  local IFS=':'
  for part in $PATH; do
    if [[ "$part" == "$HOME/.pvm/versions/python-"*/python/bin ]]; then
      continue
    fi
    new_path="${new_path:+$new_path:}$part"
  done

  PATH="$new_path"
}


__pvm_hook() {
  [[ "$PWD" == "$__PVM_LAST_PWD" ]] && return 0
  __PVM_LAST_PWD="$PWD"

  local version_file version resolved global_version

  # ---- Project-local version ----
  if version_file="$(__pvm_find_version_file)"; then
    version="$(__pvm_read_version "$version_file")"
    [[ -z "$version" ]] && return 0

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
      __pvm_restore_path
      __PVM_LAST_VERSION="$version"
      __PVM_ACTIVE_VERSION=""
    fi

    return 0
  fi

  # ---- Global fallback ----
  if global_version="$(__pvm_read_global_version)"; then
    resolved="$(__pvm_resolve_version "$global_version")"

    if [[ "$resolved" == "$__PVM_ACTIVE_VERSION" ]]; then
      __PVM_LAST_VERSION="global:$global_version"
      return 0
    fi

    if [[ -n "$resolved" ]]; then
      __pvm_prepend_version "$HOME/.pvm/versions/python-$resolved"
      __PVM_LAST_VERSION="global:$global_version"
      __PVM_ACTIVE_VERSION="$resolved"
      return 0
    fi
  fi

  # ---- System fallback ----
  __pvm_restore_path
  __PVM_LAST_VERSION=""
  __PVM_ACTIVE_VERSION=""
}


if [[ -n "$BASH_VERSION" ]]; then
  PROMPT_COMMAND="__pvm_hook${PROMPT_COMMAND:+;$PROMPT_COMMAND}"
fi

if [[ -n "$ZSH_VERSION" ]]; then
  autoload -Uz add-zsh-hook
  add-zsh-hook chpwd __pvm_hook
  __pvm_hook
fi


__pvm_resolve_version() {
  local required="$1"
  local base="$HOME/.pvm/versions"
  local best=""

  # Ensure glob behaves the same in zsh and bash
  setopt localoptions nullglob 2>/dev/null

  for d in "$base"/python-*; do
    [[ -d "$d" ]] || continue

    local v="${d##*/python-}"

    if __pvm_version_matches "$required" "$v"; then
      if [[ -z "$best" ]]; then
        best="$v"
      else
        best="$(printf '%s\n%s\n' "$best" "$v" | sort -V | tail -n1)"
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
  PATH="$version_dir/python/bin:$PATH"
  export PATH
}


__pvm_version_matches() {
  local required="$1"
  local active="$2"

  [[ "$active" == "$required" || "$active" == "$required".* ]]
}


python() {
  # Only warn if a .python-version exists for this directory
  if [[ -n "$__PVM_LAST_VERSION" && -z "$__PVM_ACTIVE_VERSION" ]]; then
    echo "pvm: warning: python version '$__PVM_LAST_VERSION' is required but not installed" >&2
  fi

  # Call the actual python in PATH (could be system Python or already set via __pvm_hook)
  command python "$@"
}

#just a pvm wrapper to exec print commands