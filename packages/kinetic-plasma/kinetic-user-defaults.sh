# ZypherOS Kinetic: apply Kinetic's per-user defaults, such as keyboard
# shortcuts, before Plasma's services start
if [ -x /usr/libexec/kinetic/user-defaults ]; then
	/usr/libexec/kinetic/user-defaults
fi
