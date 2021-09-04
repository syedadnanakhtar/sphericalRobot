/opt/vc/bin/raspivid -t 0 -w 1280 -h 720 -ih -fps 20 -vf -hf  -n -o - | nc -k -l 8090
