#!/sbin/busybox sh

while ! busybox grep "/mnt/external_sd" /proc/mounts > /dev/null
do
	busybox sleep 1
done

srcd=/mnt/ram/
dstd=/mnt/external_sd/dumps
busybox mkdir -p $dstd
busybox rm $dstd/dump.* 
busybox rm /mnt/external_sd/RetroFreak/Games/* 
# copy log files(/mnt/ram/log/*) to SD(/retrofd/log) if new ones exist
while : ;
do
	busybox find $srcd -maxdepth 1 -type f | busybox sed -e 's/.*\///' | while read logfile
	do
		[ -f "$dstd/$logfile" ] || busybox sleep 5 && busybox cp "$srcd/$logfile" "$dstd/${edump}"  
	done
                            edump=`busybox ls /mnt/external_sd/RetroFreak/Games/`
                            busybox rm /mnt/external_sd/RetroFreak/Games/*
                            busybox rm $dstd/dump.* 
	busybox sleep 1
done
