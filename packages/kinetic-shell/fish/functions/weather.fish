function weather --description 'Show the weather from wttr.in'
    if test (count $argv) -gt 0
        curl -s "wttr.in/$argv[1]"
    else
        curl -s "wttr.in"
    end
end
