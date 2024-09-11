grep -Psil '^\h*\[xdmcp\]' /etc/{gdm3,gdm}/{custom,daemon}.conf | while IFS= read -r l_file; do
  awk -v file="$l_file" '
    /^\[xdmcp\]/{ f = 1; next }
    /^\[/{ f = 0 }
    f && /^\s*Enable\s*=\s*true/ {
      print "The file: \"" file "\" includes: \"" $0 "\" in the \"[xdmcp]\" block"
    }
  ' "$l_file"
done
