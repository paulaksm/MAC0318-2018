#!/bin/bash
while true
do
    /opt/vc/bin/vcgencmd measure_temp
    sleep 3
done
