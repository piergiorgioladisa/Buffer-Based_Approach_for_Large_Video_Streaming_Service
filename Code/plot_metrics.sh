
#!/bin/bash
#log_filename="../../tapas-master/logs/conventional/bydefault.log"
#log_filename="../../tapas-master/logs/conventional/rate_based.log"

if [ ! -z $1 ]
then
log_filename="../../tapas-master/logs/BBA0/$1"
else
log_filename="../../tapas-master/logs/BBA0/$(ls ../../tapas-master/logs/BBA0  -Art | tail -n 1)"
fi
echo "Opening: $log_filename"

cp "$log_filename" test.csv
log_fileName="test.csv"

# Modify time from absolute to relative
IFS=","
i=0
while read line
do
IFS=' ' read -r -a array <<< "$line"
time_abs[$i]=${array[0]}
let i++
done < $log_fileName
echo ${time_abs[@]} > time_abs.csv

time_rel[0]=${time_abs[0]}
for (( i=1 ; i<=${#time_abs[@]}-1 ; i++ )) ; do
time_rel[$i]=`echo "${time_abs[$i]} - ${time_abs[1]}" | bc`
done
echo " ${time_rel[@]/%/$'\n'}" > time_rel.csv

in2csv $log_fileName -d " " > "testc.csv"
csvcut -C 1 "testc.csv" > $log_fileName
in2csv 'time_rel.csv' -d " " > 'time_relc.csv'
csvcut -C 1 'time_relc.csv' > 'time_rel.csv'
csvjoin 'time_rel.csv' $log_fileName > "testc.csv"
csvformat -D " " "testc.csv" > $log_fileName

#read -p "Press Enter to continue" </dev/tty

# find when it gets on
IFS=","
first_on_index=1
while read line
do
IFS=' ' read -r -a array <<< "$line"
if [[ ! -z "${line// }" ]]
then
player_status=${array[7]}
if [ "$player_status" != "True" ]
then
first_on_time=${array[0]}
let first_on_index++
fi
fi
done < $log_fileName

echo $first_on_index
echo $first_on_time

# plot

gnuplot -e "
filename = '$log_fileName';
x_label = '$first_on_time';
set grid;
set title 'Network and video player metrics';
set xlabel 'time (s)';
set label 'ON' at x_label, 1;
plot filename u 1:3 w lp t 'enqueud_t (s)', filename u 1:4 w lp t 'bwe (Mbps)', filename u 1:5 w lp t 'video rate (Mbps)';
pause -1;
exit
"
