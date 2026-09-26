function ff --description 'Find files whose name contains the argument'
    find . -type f -name "*$argv*" 2>/dev/null
end
