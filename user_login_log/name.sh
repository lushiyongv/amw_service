cat *.log | awk -F '\t' '{print $(NF-0)}' | sort | uniq -c | wc -l
