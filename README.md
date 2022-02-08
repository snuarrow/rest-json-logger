# rest-json-logger

firstly make config file, use "config_example.json" as base

for looped run
```
conda env update -f cenv.yaml -n rest-json-logger
python log.py --config-file <file_path> --loop
```

enabling cron task
```
sudo service cron status
crontab -e
add to crontab: * * * * * /bin/sh /home/<your_username>/rest-json-logger/cron.sh
see stdout from 'cron_stdout.txt'
```
