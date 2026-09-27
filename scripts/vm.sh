#!/usr/bin/env bash
# Test the Kinetic ISO in a KVM virtual machine (no root needed).
# UEFI with Secure Boot enabled, 8 GB RAM, 4 CPUs, a 64 GB virtual disk.
#
#   ./scripts/vm.sh start              # boot the ISO in a window; install to the virtual disk from there
#   ./scripts/vm.sh start --disk       # boot the installed virtual disk
#   ./scripts/vm.sh start --headless   # no window; drive it with screenshot/key
#   ./scripts/vm.sh start --tpm        # add a TPM 2.0 (swtpm), for disk unlock tests
#   ./scripts/vm.sh start --iso FILE   # boot another ISO than this version's
#   ./scripts/vm.sh ssh [COMMAND]      # ssh in as the VM's user (KINETIC_VM_USER, default "tester")
#   ./scripts/vm.sh screenshot FILE.png
#   ./scripts/vm.sh key ret            # send keys (QEMU sendkey names, e.g. ctrl-alt-f2)
#   ./scripts/vm.sh type "some text"   # type text into the VM
#   ./scripts/vm.sh click X Y          # click at screen pixel X,Y (as in screenshots)
#   ./scripts/vm.sh stop
#   ./scripts/vm.sh reset              # delete the virtual disk, firmware settings, and TPM
#
# The VM's SSH port is forwarded to 127.0.0.1:22022 (KINETIC_VM_SSH_PORT) only. To
# use "vm.sh ssh", enable sshd in the VM and add out/vm/ssh_key.pub to the
# user's ~/.ssh/authorized_keys ("vm.sh ssh" prints how).
set -euo pipefail

source "$(dirname "${BASH_SOURCE[0]}")/common.sh"

vm_dir="${KINETIC_OUT}/vm"
disk="${vm_dir}/disk.qcow2"
vars="${vm_dir}/OVMF_VARS.fd"
monitor="${vm_dir}/monitor.sock"
qmp="${vm_dir}/qmp.sock"
tpm_dir="${vm_dir}/tpm"
ssh_key="${vm_dir}/ssh_key"
ssh_port="${KINETIC_VM_SSH_PORT:-22022}"
ssh_opts=(-q -i "${ssh_key}" -p "${ssh_port}" -l "${KINETIC_VM_USER:-tester}"
	-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null)
ovmf_dir="/usr/share/edk2/ovmf"

monitor_cmd() {
	[[ -S "${monitor}" ]] || { echo "VM is not running" >&2; exit 1; }
	printf '%s\n' "$1" | socat - "UNIX-CONNECT:${monitor}" >/dev/null
}

start() {
	local boot_iso=1 headless=0 tpm=0 iso="${KINETIC_ISO}"
	while (($#)); do
		case "$1" in
			--disk) boot_iso=0 ;;
			--headless) headless=1 ;;
			--tpm) tpm=1 ;;
			--iso) iso="${2:?--iso needs a file}"; shift ;;
			*) echo "Unknown option: $1" >&2; exit 2 ;;
		esac
		shift
	done

	mkdir -p "${vm_dir}"
	[[ -f "${disk}" ]] || qemu-img create -q -f qcow2 "${disk}" 64G
	[[ -f "${vars}" ]] || cp "${ovmf_dir}/OVMF_VARS.secboot.fd" "${vars}"

	local args=(
		-name kinetic
		-machine q35,smm=on,accel=kvm
		-cpu host -smp 4 -m 8G
		-global driver=cfi.pflash01,property=secure,value=on
		-drive "if=pflash,format=raw,unit=0,readonly=on,file=${ovmf_dir}/OVMF_CODE.secboot.fd"
		-drive "if=pflash,format=raw,unit=1,file=${vars}"
		-drive "file=${disk},if=virtio,format=qcow2"
		-nic "user,model=virtio-net-pci,hostfwd=tcp:127.0.0.1:${ssh_port}-:22"
		-device virtio-vga
		-device qemu-xhci -device usb-tablet
		-monitor "unix:${monitor},server,nowait"
		-qmp "unix:${qmp},server,nowait"
		-serial "file:${vm_dir}/serial.log"
	)
	if ((boot_iso)); then
		[[ -f "${iso}" ]] || { echo "No ISO at ${iso}; build it first" >&2; exit 1; }
		args+=(-drive "file=${iso},media=cdrom,readonly=on" -boot order=d)
	fi
	if ((tpm)); then
		# The TPM's state persists in out/vm/tpm, like the disk
		mkdir -p "${tpm_dir}"
		swtpm socket --tpm2 --daemon --terminate \
			--tpmstate "dir=${tpm_dir}" \
			--ctrl "type=unixio,path=${tpm_dir}/swtpm.sock"
		args+=(-chardev "socket,id=chrtpm,path=${tpm_dir}/swtpm.sock"
			-tpmdev emulator,id=tpm0,chardev=chrtpm -device tpm-crb,tpmdev=tpm0)
	fi
	if ((headless)); then
		args+=(-display none -daemonize -pidfile "${vm_dir}/qemu.pid")
	else
		args+=(-display gtk)
	fi

	qemu-system-x86_64 "${args[@]}"
}

case "${1:-}" in
	start) shift; start "$@" ;;
	screenshot)
		out="${2:?usage: vm.sh screenshot FILE.png}"
		ppm="$(mktemp --suffix=.ppm)"
		monitor_cmd "screendump ${ppm}"
		sleep 1
		magick "${ppm}" "${out}"
		rm -f "${ppm}"
		;;
	key) shift; for k in "$@"; do monitor_cmd "sendkey ${k}"; sleep 0.2; done ;;
	type)
		text="${2:?usage: vm.sh type TEXT}"
		for ((i = 0; i < ${#text}; i++)); do
			c="${text:i:1}"
			case "${c}" in
				[a-z0-9]) k="${c}" ;;
				[A-Z]) k="shift-${c,,}" ;;
				' ') k="spc" ;; '-') k="minus" ;; '_') k="shift-minus" ;; '.') k="dot" ;;
				'/') k="slash" ;; ':') k="shift-semicolon" ;; ';') k="semicolon" ;; '|') k="shift-backslash" ;;
				'=') k="equal" ;; ',') k="comma" ;; "'") k="apostrophe" ;; '"') k="shift-apostrophe" ;;
				'>') k="shift-dot" ;; '<') k="shift-comma" ;; '&') k="shift-7" ;; '*') k="shift-8" ;;
				'[') k="bracket_left" ;; ']') k="bracket_right" ;; '{') k="shift-bracket_left" ;; '}') k="shift-bracket_right" ;;
				'(') k="shift-9" ;; ')') k="shift-0" ;; '\') k="backslash" ;; '%') k="shift-5" ;; '$') k="shift-4" ;;
				'#') k="shift-3" ;; '@') k="shift-2" ;; '!') k="shift-1" ;; '+') k="shift-equal" ;; '?') k="shift-slash" ;;
				'~') k="shift-grave_accent" ;; '`') k="grave_accent" ;; '^') k="shift-6" ;;
				*) echo "vm.sh type: unsupported character '${c}'" >&2; exit 2 ;;
			esac
			monitor_cmd "sendkey ${k}"
			# A busy guest drops keys typed faster than this
			sleep 0.04
		done
		;;
	click)
		x="${2:?usage: vm.sh click X Y}"; y="${3:?usage: vm.sh click X Y}"
		[[ -S "${qmp}" ]] || { echo "VM is not running" >&2; exit 1; }
		# Absolute pointer coordinates run 0-32767 across the current screen size
		ppm="$(mktemp --suffix=.ppm)"
		monitor_cmd "screendump ${ppm}"
		sleep 0.5
		read -r width height < <(identify -format '%w %h\n' "${ppm}")
		rm -f "${ppm}"
		python3 - "${qmp}" "${x}" "${y}" "${width}" "${height}" <<'PY'
import json, socket, sys, time
path, x, y, w, h = sys.argv[1], *map(int, sys.argv[2:6])
s = socket.socket(socket.AF_UNIX); s.connect(path); f = s.makefile("rw")
def cmd(obj):
    f.write(json.dumps(obj) + "\n"); f.flush()
    while "return" not in (reply := json.loads(f.readline())) and "error" not in reply:
        pass
    return reply
json.loads(f.readline())
cmd({"execute": "qmp_capabilities"})
ax, ay = x * 32767 // (w - 1), y * 32767 // (h - 1)
cmd({"execute": "input-send-event", "arguments": {"events": [
    {"type": "abs", "data": {"axis": "x", "value": ax}},
    {"type": "abs", "data": {"axis": "y", "value": ay}}]}})
time.sleep(0.1)
for down in (True, False):
    cmd({"execute": "input-send-event", "arguments": {"events": [
        {"type": "btn", "data": {"down": down, "button": "left"}}]}})
    time.sleep(0.08)
PY
		;;
	ssh)
		shift
		[[ -f "${ssh_key}" ]] || ssh-keygen -q -t ed25519 -N "" -C kinetic-vm-test -f "${ssh_key}"
		if ! ssh -n "${ssh_opts[@]}" -o BatchMode=yes -o ConnectTimeout=5 localhost true 2>/dev/null; then
			echo "Can't log in to the VM over SSH yet. In the VM, run:" >&2
			echo "  sudo systemctl enable --now sshd" >&2
			echo "  mkdir -p ~/.ssh && echo '$(cat "${ssh_key}.pub")' >> ~/.ssh/authorized_keys" >&2
			exit 1
		fi
		exec ssh "${ssh_opts[@]}" localhost "$@"
		;;
	stop) monitor_cmd "quit" ;;
	reset) rm -rf "${disk}" "${vars}" "${tpm_dir}"; echo "Virtual disk, firmware settings, and TPM removed" ;;
	*) awk 'NR > 1 && /^#/ { sub(/^# ?/, ""); print; next } NR > 1 { exit }' "$0"; exit 2 ;;
esac
