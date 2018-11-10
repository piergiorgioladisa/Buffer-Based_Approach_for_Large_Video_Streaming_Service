#!/bin/bash
#log_filename="../../tapas-master/logs/conventional/bydefault.log"
#log_filename="../../tapas-master/logs/conventional/rate_based.log"

if [ ! -z $1 ]
then
log_filename="../../tapas-master/logs/BBA0/$1"
else
log_filename="../../tapas-master/logs/BBA0/$(ls ../../tapas-master/logs/BBA0 -Art | tail -n 1)"
fi
echo "Opening: $log_filename"



winidterm=$(xdotool search --onlyvisible --name rt)
IFS=","
seg_index=0
byterange_previous=0
i=1
while read line
do
IFS=' ' read -r -a array <<< "$line"
level=${array[5]}
byterange_current=${array[17]}
let i++
if [ $i -lt 2 ]
then
byterange_previous=$byterange_current
elif [ $seg_index -lt 30 ]
then
if [ "$byterange_current" != "$byterange_previous" ]
then
echo $seg_index
echo $level
#echo $byterange_current
#echo $byterange_previous
byterange_previous=$byterange_current
segment_name=$(printf '/home/rt/Documents/scripts/segments_quality%d/video_quality%d_seg%d.mp4' "$level" "$level" "$seg_index")
gst-launch-0.10 playbin2 uri=file:"$segment_name" &
xdotool type --delay 100 --window $winidterm 'RRR\n'
winid=$(xdotool search --onlyvisible --name "gst")
xdotool windowsize $winid 1920 1080 #1360 768
wait
#read -p "Press Enter to continue" </dev/tty
let seg_index++
fi
fi

done < $log_filename


