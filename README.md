# rest-json-logger

firstly download and install miniconda, then make a config file, use "config_example.json" as base

for looped run
```
conda env update -f cenv.yaml -n rest-json-logger
conda activate rest-json-logger
python main.py --config-file <file_path> --loop
```

enabling cron task (you need to edit the cron.sh to use your config file)
```
sudo service cron status
crontab -e
add to crontab: * * * * * /bin/sh /home/<your_username>/rest-json-logger/cron.sh
see stdout from 'cron_stdout.txt'
```
