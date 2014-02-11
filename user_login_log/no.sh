cat *.log | awk -F '\t' '{print $(NF-1)}' | sort | uniq -c | wc -l
