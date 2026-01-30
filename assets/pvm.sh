pvm() {
  if [ "$1" = "use" ] || [ "$1" = "deactivate" ]; then
    eval "$(command pvm "$@")"
  else
    command pvm "$@"
  fi
}