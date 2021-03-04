# Pi-Station
Repository for all the projects I implement on my Home Pi

### The cron job that is set right now
---
```console
*/10**** /bin/bash /home/orwell/weather_runner.sh
```
- To allow the cron job to run as a sudoer we need to edit the sudo file by appending this. 

```console
    orwell ALL = NO PASSWD: /bin/python3
```
