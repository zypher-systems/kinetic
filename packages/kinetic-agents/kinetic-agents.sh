# ZypherOS Kinetic: CLI coding agents.
# Per-user agent installs come first. The Kinetic launchers at the end of
# PATH install an agent from its official source the first time it runs.
for dir in "${HOME}/.opencode/bin" "${HOME}/.grok/bin"; do
	case ":${PATH}:" in
		*":${dir}:"*) ;;
		*) [ -d "${dir}" ] && PATH="${dir}:${PATH}" ;;
	esac
done
case ":${PATH}:" in
	*":/usr/libexec/kinetic/agents:"*) ;;
	*) PATH="${PATH}:/usr/libexec/kinetic/agents" ;;
esac
export PATH
