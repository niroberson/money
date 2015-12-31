(awk 'BEGIN { FS=OFS= } { for(i = 1; i <= NF; i += 2) { gsub(", , /etc/profile.d/*.sh); } print }' NodeInRelsFixed1.csv > NodeInRelsFixed3.csv)
