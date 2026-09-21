#!/usr/bin/env bash
# Read-only guest observations for the real unsaved-document logout replay.
# This does not initiate logout, manipulate notifications, or prove image contents.
set -Eeuo pipefail
[[ $USER == aero7test && ${XDG_SESSION_TYPE:-} == wayland ]] || exit 2
[[ $(</proc/sys/kernel/hostname) == aero7-r10-offline ]] || exit 2
[[ $(find /sys/class/net -mindepth 1 -maxdepth 1 -printf '%f\n') == lo ]] || exit 2
[[ $(pacman -Q kwin) == 'kwin 6.7.4-7.1' ]] || exit 2
mountpoint -q /mnt/a7-results
phase=${1:?Supply begin, mark-after-cancel or finish}

identity() {
    local name=$1 pid=$2 stat
    [[ $pid =~ ^[1-9][0-9]*$ ]] || return 1
    # A protected process's proc directory may be root-owned even while the
    # process belongs to this user. Inspect its real UID, not proc inode ownership.
    [[ $(awk '/^Uid:/ {print $2; exit}' "/proc/$pid/status") == "$UID" ]] || return 1
    stat=$(<"/proc/$pid/stat")
    # Remove pid and the parenthesized comm, which can itself contain spaces.
    stat=${stat##*) }
    local -a fields
    read -r -a fields <<< "$stat"
    [[ ${fields[0]} != Z && ${fields[19]} =~ ^[0-9]+$ ]] || return 1
    printf '%s\t%s\t%s\n' "$name" "$pid" "${fields[19]}"
}

snapshot() {
    local destination=$1
    mkdir "$destination"
    date -Is > "$destination/time.txt"
    cut -d ' ' -f1 /proc/uptime > "$destination/uptime.txt"
    cat /proc/sys/kernel/random/boot_id > "$destination/boot.txt"
    printf '%s\n' "${XDG_SESSION_ID:?}" > "$destination/session.txt"
    loginctl show-session "$XDG_SESSION_ID" -p Id -p Active -p State -p Leader -p Timestamp > "$destination/session-details.txt"
    [[ $(loginctl show-session "$XDG_SESSION_ID" -p Active --value) == yes ]]
    systemctl --user is-active --quiet aero7-shell.service
    identity shell "$(systemctl --user show aero7-shell.service -p MainPID --value)" > "$destination/processes.tsv"
    identity compositor "$(pgrep -u "$UID" -x kwin_wayland)" >> "$destination/processes.tsv"
    identity paint "$(pgrep -u "$UID" -x kolourpaint)" >> "$destination/processes.tsv"
    systemctl --user show aero7-shell.service plasma-plasmashell.service -p Id -p MainPID -p ActiveState -p NRestarts > "$destination/services.txt"
    systemctl --user --failed --no-pager > "$destination/failed-user-units.txt"
    systemctl --failed --no-pager > "$destination/failed-system-units.txt"
    journalctl --user -b --no-pager > "$destination/user-journal.txt"
}

if [[ $phase == begin ]]; then
    [[ $# == 1 ]] || exit 2
    report=$(mktemp -d /mnt/a7-results/kwin-logout-deadline.XXXXXX)
    snapshot "$report/before"
    printf 'REPORT=%s\n' "$report"
    printf 'Before logout recorded. After cancelling the document prompt, run mark-after-cancel with this report path.\n'
    exit 0
fi

[[ $# == 2 ]] || exit 2
report=$(realpath -e "$2")
[[ $report == /mnt/a7-results/kwin-logout-deadline.* && ${report#/mnt/a7-results/} != */* ]] || exit 2
[[ -d $report/before && $(stat -c %u "$report") == "$UID" ]] || exit 2
case $phase in
    mark-after-cancel) destination=after-cancel ;;
    finish) [[ -d $report/after-cancel ]] || exit 2; destination=after-deadline ;;
    *) exit 2 ;;
esac
snapshot "$report/$destination"
for record in boot.txt session.txt processes.tsv; do
    cmp "$report/before/$record" "$report/$destination/$record"
done
if [[ $phase == finish ]]; then
    awk 'NR == 1 {start=$1; next} {elapsed=$1-start; printf "SECONDS_SINCE_DOCUMENT_CANCEL=%.2f\n", elapsed; exit(elapsed < 150)}' \
        "$report/after-cancel/uptime.txt" "$report/after-deadline/uptime.txt" | tee "$report/elapsed.txt"
    printf 'SAME_BOOT_SESSION_COMPOSITOR_SHELL_AND_PAINT_SURVIVED_DEADLINE\n' | tee "$report/result.txt"
    printf 'Still required: visually verify the unsaved drawing, save it normally and inspect the resulting PNG.\n'
else
    printf 'CANCEL_MARK_RECORDED; wait at least 150 real seconds before finish.\n'
fi
