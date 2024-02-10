# Current setup on my Raspberry Pi

Cross-compile and copy programs and make them available in $PATH.

Copy the website files:
```
# do NOT use --delete, since currently the dynamically generated graphs
# and archives are also stored under the www directory
rsync -v -rtlp www pi:./
```

Create base directories and setup:
```
mkdir -p /home/pi/observations
apt install nginx-light
cp nginx-sites-temperature /etc/nginx/sites-available/temperature
# ... and remove the default site, link the "temperature" site, reload nginx
```

Launch tmux and run:
* `./probe-dht.sh`
* `./probe-msc.sh`
* `./regenerate-graphs.sh`

*or* copy the systemd unit files to /etc/systemd/system and start and enable
them.
