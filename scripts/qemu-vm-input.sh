#!/usr/bin/env bash
set -Eeuo pipefail

qemu_runtime_root="${XDG_RUNTIME_DIR:-/tmp}/aero7-qemu-$UID"
qmp_socket="$qemu_runtime_root/qmp.sock"
hmp_socket="$qemu_runtime_root/monitor.sock"

usage() {
  printf 'Usage: %s click X Y | key QEMU_KEY | text TEXT\n' "${0##*/}" >&2
  exit 2
}

[[ -S "$qmp_socket" && -S "$hmp_socket" ]] || {
  printf 'The Aero7 QEMU monitor sockets are not available.\n' >&2
  exit 1
}
command -v nc >/dev/null 2>&1 || {
  printf 'The QEMU input helper requires netcat (nc).\n' >&2
  exit 1
}

qmp_event() {
  local event="$1"
  printf '%s\n' '{"execute":"qmp_capabilities"}' "$event" |
    nc -N -U "$qmp_socket" >/dev/null
}

case "${1:-}" in
  click)
    [[ "${2:-}" =~ ^[0-9]+$ && "${3:-}" =~ ^[0-9]+$ ]] || usage
    x="$2"
    y="$3"
    ((x >= 0 && x < 1024 && y >= 0 && y < 768)) || usage
    qx=$((x * 32767 / 1024))
    qy=$((y * 32767 / 768))
    qmp_event "{\"execute\":\"input-send-event\",\"arguments\":{\"events\":[{\"type\":\"abs\",\"data\":{\"axis\":\"x\",\"value\":$qx}},{\"type\":\"abs\",\"data\":{\"axis\":\"y\",\"value\":$qy}}]}}"
    sleep 0.1
    qmp_event '{"execute":"input-send-event","arguments":{"events":[{"type":"btn","data":{"down":true,"button":"left"}}]}}'
    sleep 0.15
    qmp_event '{"execute":"input-send-event","arguments":{"events":[{"type":"btn","data":{"down":false,"button":"left"}}]}}'
    ;;
  key)
    [[ -n "${2:-}" && -z "${3:-}" ]] || usage
    printf 'sendkey %s 80\n' "$2" | nc -N -U "$hmp_socket" >/dev/null
    ;;
  text)
    [[ -n "${2:-}" && -z "${3:-}" ]] || usage
    value="$2"
    {
      for ((index = 0; index < ${#value}; index++)); do
        character="${value:index:1}"
        case "$character" in
          [a-z0-9]) key_name="$character" ;;
          [A-Z]) key_name="shift-${character,,}" ;;
          ' ') key_name=spc ;;
          '-') key_name=minus ;;
          '_') key_name=shift-minus ;;
          '.') key_name='dot' ;;
          '/') key_name=slash ;;
          ':') key_name=shift-semicolon ;;
          '=') key_name=equal ;;
          '+') key_name=shift-equal ;;
          ',') key_name=comma ;;
          '@') key_name=shift-2 ;;
          '~') key_name=shift-grave_accent ;;
          *)
            printf 'Unsupported text character for QEMU input: %q\n' "$character" >&2
            exit 2
            ;;
        esac
        printf 'sendkey %s 60\n' "$key_name"
        sleep 0.16
      done
    } | nc -N -U "$hmp_socket" >/dev/null
    ;;
  *) usage ;;
esac
