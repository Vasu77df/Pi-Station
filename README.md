# Pi-Station
Repository for all the projects I implement on my Home Pi more stuff coming in the future.

-  setting a cron job that runs every 10th min to fetch weather and time data as it is constant 
    refreshing of the E-Ink display can lead to failures 

```console
*/10**** /bin/bash /home/orwell/weather_runner.sh
```
- To allow the cron job to run as a sudoer we need to edit the sudo file by appending this. 

```console
    orwell ALL = NO PASSWD: /bin/python3
```

- Also you have to move the meteocon.ttf icons file to this directory to run the script as cron job
```console
    /usr/share/fonts/truetype/meteocon/meteocons.ttf
```
