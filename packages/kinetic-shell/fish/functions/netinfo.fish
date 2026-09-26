function netinfo --description 'Show external IP, local IP, and DNS server'
    echo "🌐 Network Information:"
    echo "External IP: "(curl -s ifconfig.me)
    echo "Local IP: "(ip route get 1.1.1.1 | string match -rg 'src (\S+)')
    echo "DNS: "(resolvectl dns 2>/dev/null | string match -rg ':\s+(\S+)' | head -1)
end
