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

__PVM_LAST_REQUESTED=""
__PVM_WARNED_VERSION=""
__PVM_ACTIVE_VENV=""

__pvm_read_version_file() {
  local file="$1"
  [[ -f "$file" ]] || return 1

  local line
  IFS= read -r line < "$file" || return 1

  # strip comments
  line="${line%%#*}"
  # trim leading whitespace
  line="${line#"${line%%[![:space:]]*}"}"
  # trim trailing whitespace
  line="${line%"${line##*[![:space:]]}"}"

  [[ -n "$line" ]] && printf '%s\n' "$line"
}

__pvm_find_venv() {
  for name in .venv venv; do
    for sub in bin Scripts; do
      if [[ -f "$PWD/$name/$sub/activate" ]]; then
        echo "$PWD/$name/$sub/activate"
        return 0
      fi
    done
  done
  return 1
}

__pvm_hook() {
  local version required_version venv

  # ---- 1. Local virtualenv ----
  for name in .venv venv; do
    if [[ -f "$PWD/$name/bin/activate" ]]; then
      venv="$PWD/$name"
      break
    fi
  done

  if activate_script="$(__pvm_find_venv)"; then
    if [[ "$__PVM_ACTIVE_VENV" != "$activate_script" ]]; then
      if command -v deactivate >/dev/null 2>&1; then
        deactivate
      fi

      # shellcheck disable=SC1090
      source "$activate_script"
      __PVM_ACTIVE_VENV="$activate_script"
    fi
    return
  fi

  # Leaving venv project
  if [[ -n "$__PVM_ACTIVE_VENV" ]]; then
    deactivate 2>/dev/null
    __PVM_ACTIVE_VENV=""
  fi

  # ---- 2. Project version file ----
  if required_version="$(__pvm_read_version_file "$PWD/.python-version")"; then
    if [[ "$required_version" != "$__PVM_LAST_REQUESTED" ]]; then
      eval "$(pvm use "$required_version")"
      __PVM_LAST_REQUESTED="$required_version"
      __PVM_WARNED_VERSION=""
    fi
  # ---- 3. Global fallback ----
  elif required_version="$(__pvm_read_version_file "$HOME/.pvm/bin/global-version")"; then
    if [[ "global:$required_version" != "$__PVM_LAST_REQUESTED" ]]; then
      eval "$(pvm use "$required_version")"
      __PVM_LAST_REQUESTED="global:$required_version"
      __PVM_WARNED_VERSION=""
    fi
  else
    # No version requirement
    if [[ -n "$__PVM_LAST_REQUESTED" ]]; then
      eval "$(pvm deactivate)"
      __PVM_LAST_REQUESTED=""
      __PVM_WARNED_VERSION=""
    fi
    return
  fi

  # ---- 4. Mismatch Warning ----
  if [[ -n "$required_version" ]]; then
#    current_version="$(python -V 2>&1 | awk '{print $2}')"
    current_version="$(python -V 2>&1)"
    current_version="${current_version#Python }"

    if [[ "$current_version" != "$required_version"* ]]; then
      if [[ "$__PVM_WARNED_VERSION" != "$required_version" ]]; then
        echo -e "\033[0;31mpvm: warning: python '$required_version' required but current is '$current_version'\033[0m" >&2
        __PVM_WARNED_VERSION="$required_version"
      fi
    fi
  fi
}

if [[ -n "$BASH_VERSION" ]]; then
  PROMPT_COMMAND="__pvm_hook${PROMPT_COMMAND:+;$PROMPT_COMMAND}"
fi

if [[ -n "$ZSH_VERSION" ]]; then
  autoload -Uz add-zsh-hook
  add-zsh-hook chpwd __pvm_hook
  add-zsh-hook precmd __pvm_hook
fi