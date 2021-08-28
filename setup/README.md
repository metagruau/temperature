# Current local setup

Copy and compile programs and make them available in $PATH.

Create base directories and setup:
```
mkdir -p /home/pi/observations /home/pi/www
apt-get install nginx-light
cp nginx-sites-temperature /etc/nginx/sites-available/temperature
# ... and remove the default site, link the "temperature" site, reload nginx
```

Launch tmux and run:
* `./probe-dht.sh`
* `./probe-msc.sh`
* `./regenerate-graphs.sh`
