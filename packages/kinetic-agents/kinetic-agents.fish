# ZypherOS Kinetic: CLI coding agents (see /etc/profile.d/kinetic-agents.sh).
# Per-user agent installs come first; the Kinetic launchers come last.
fish_add_path --global --path $HOME/.opencode/bin $HOME/.grok/bin
fish_add_path --global --path --append /usr/libexec/kinetic/agents
