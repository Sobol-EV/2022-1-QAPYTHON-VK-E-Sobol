#! /bin/bash

file_path=$1
file_output=$2
method='"CONNECT |"OPTIONS |"HEAD |"DELETE |"PUT |"POST |"GET |'
total_request=0
counter=0
IFS="|"
read -a Arr <<< "$method"
echo "--> Number of requests by request method type:" > $file_output
for i in "${Arr[@]}";
do
    let "counter = $(grep -c $i $file_path)"
    echo "Method ${i:1:-1} meets $counter." >> $file_output
    let "total_request += counter"
done

echo "--> Total Requests: $total_request." >> $file_output

echo "--> Top 10 most frequent requests:" >> $file_output
tail -$total_request $file_path | awk '{freq[$7]++} END {for (x in freq) {print freq[x], x}}' | sort -rn | head -10 >> $file_output

echo "--> Top 5 Largest Shipments Covered by Client (4XX) Error:" >> $file_output
tail -$total_request $file_path | awk '{split($9,a,""); if (a[1] == 4) {freq_url[$1]=$7; freq_code[$1]=$9; freq_length[$1]=length($7) }} END {for (x in freq_length) {print freq_length[x], freq_code[x], x, freq_url[x]}}'  | sort -rn | head -5 >> $file_output

echo "--> Top 5 users by number of requests that ended with a server (5XX) error:" >> $file_output
tail -$total_request $file_path | awk '{split($9,a,""); if (a[1] == 5) freq[$1]++} END {for (x in freq) {print freq[x], x}}' | sort -rn | head -5 >> $file_output
