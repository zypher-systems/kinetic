# ===============================================
# ZypherOS Kinetic - fish defaults (all users)
# ===============================================
# Loaded from vendor_conf.d before your own ~/.config/fish/config.fish,
# so anything you set there wins. Based on the Zypher Systems fish
# configuration.

# ===== PATH (every shell, not only interactive ones) =====
fish_add_path --global --path $HOME/.local/bin
test -f $HOME/.cargo/env.fish; and source $HOME/.cargo/env.fish

if not status is-interactive
    return
end

# ===== ENVIRONMENT =====
set -q EDITOR; or set -gx EDITOR nvim
set -gx PAGER less
set -gx MANPAGER "sh -c 'col -bx | bat -l man -p'"
set -gx COLORTERM truecolor
set -gx CLICOLOR 1
set -gx LS_COLORS "di=1;36:ln=1;35:so=1;32:pi=1;33:ex=1;31:bd=1;34:cd=1;34:su=0;41:sg=0;46:tw=0;42:ow=0;43"

# ===== KEY BINDINGS AND COLORS =====
fish_vi_key_bindings

set -g fish_color_normal normal
set -g fish_color_command 00d7ff
set -g fish_color_quote a8cc8c
set -g fish_color_redirection ff6b9d
set -g fish_color_end ff6b9d
set -g fish_color_error ff5555
set -g fish_color_param d7d7d7
set -g fish_color_comment 6272a4
set -g fish_color_match --background=brblue
set -g fish_color_selection white --bold --background=brblack
set -g fish_color_search_match bryellow --background=brblack
set -g fish_color_history_current --bold
set -g fish_color_operator ff79c6
set -g fish_color_escape 8be9fd
set -g fish_color_cwd green
set -g fish_color_cwd_root red
set -g fish_color_valid_path --underline
set -g fish_color_autosuggestion 6272a4
set -g fish_color_user brgreen
set -g fish_color_host normal
set -g fish_color_cancel -r
set -g fish_pager_color_completion normal
set -g fish_pager_color_description B3A06D yellow
set -g fish_pager_color_prefix white --bold --underline
set -g fish_pager_color_progress brwhite --background=cyan

# ===== ALIASES =====
# Listing (colors only when writing to a terminal, so pipes stay clean)
alias ls 'eza --color=auto --group-directories-first --icons=auto'
alias ll 'eza -alF --color=auto --group-directories-first --icons=auto'
alias la 'eza -a --color=auto --group-directories-first --icons=auto'
alias lt 'eza -aT --color=auto --group-directories-first --icons=auto'
alias l. 'eza -a | grep -E "^\."'

# Git
alias g 'git'
alias gs 'git status -sb'
alias gl 'git log --oneline --graph --decorate --all'
alias ga 'git add'
alias gc 'git commit'
alias gp 'git push'
alias gd 'git diff --color=always'

# System information
alias sysinfo 'fastfetch'
alias myip 'curl -s ifconfig.me'
alias ports 'ss -tuln'

# Viewing
alias cat 'bat --style=numbers,changes,header'
alias less 'bat --paging=always'

# Navigation
alias .. 'cd ..'
alias ... 'cd ../..'
alias .... 'cd ../../..'

# Monitoring and sizes
alias htop 'btop'
alias df 'df -h'
alias du 'du -h'
alias free 'free -h'

# Misc
alias grep 'grep --color=auto'
alias mkdir 'mkdir -pv'
alias wget 'wget -c'
alias userlist 'cut -d: -f1 /etc/passwd'
alias fsize 'du -sh'
alias reload 'source ~/.config/fish/config.fish'

# List the new directory after every directory change, without replacing
# cd, so "cd -" and fish's directory history keep working
function __kinetic_ls_after_cd --on-variable PWD
    status is-command-substitution; and return
    ls
end

# ===== PROMPT AND TOOLS =====
command -q starship; and starship init fish | source
command -q zoxide; and zoxide init fish | source

# ===== WELCOME MESSAGE =====
function fish_greeting
    set_color cyan
    echo "╭────────────────────────────────────────────────────────────╮"
    set_color --bold blue
    printf "│ 🚀 %-55s │\n" "Zypher Terminal - Enhanced Experience"
    set_color normal
    set_color yellow
    printf "│ 📅 %-55s │\n" (date "+%A, %B %d, %Y at %I:%M %p")
    set_color green
    set -l uptime_info (cut -d' ' -f1 /proc/uptime)
    set -l uptime_hours (math "floor($uptime_info / 3600)")
    set -l uptime_minutes (math "floor(($uptime_info % 3600) / 60)")
    printf "│ 💾 %-55s │\n" "Uptime: $uptime_hours hours, $uptime_minutes minutes"
    set_color magenta
    printf "│ 🖥️ %-55s │\n" "Host: "(hostname)
    set_color red
    printf "│ 👤 %-55s │\n" "User: $USER"
    set_color blue
    printf "│ 🐚 %-55s │\n" "Shell: Fish "(fish --version | string match -r '\d+\.\d+\.\d+')
    set_color cyan
    echo "╰────────────────────────────────────────────────────────────╯"
    set_color normal
    echo
    set_color --dim white
    echo "💡 Tips: Use 'sysinfo' for detailed system info, 'weather' for weather, 'netinfo' for network details"
    set_color normal
    echo
end
