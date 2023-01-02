# heatpump-logger

Logs data from Alpha Innotec heatpump to file and to Domoticz

## Introduction

Having a heatpump at work to warm your house is a great thing, but sometimes you might to have more insight in what is happening in this machine and why it operates the way it does. This logger can help you with that.

The script is set up to run on a Raspberry Pi, but you can run it on any machine with Python3.

The data points I have choosen to log can be different from what others may want to log. And that is easy to adapt in the script.

## Source of data

Data is obtained from a Alpha Innotec WZSV heatpump, using the web interface. You can check the user manual to find out how to start the webserver on the heatpump. The password you choose for the web insterface is not relevant for the heatpump-logger script, since it uses readonly access which is available without password.

## Output of data

Since I happened to run Domoticz already for my "Slimme meter" (common in the Netherlands to read data about usage of electricity and gas), it seamed a good idea to send the data Domoticz. In order to do this, you need to prepaire Domoticz for receiving data. I used this Dutch guide: http://domoticx.com/internet-of-things-domoticz-data-ontvangen-vanuit-andere-bron/](http://domoticx.com/internet-of-things-domoticz-data-ontvangen-vanuit-andere-bron/). Basically you need to create so called device numbers which can be used as a reference when you push data to Domoticz.

Apart from pushing data to Domoticz, I personally wanted to log the data to file as well, with 5 minute intervals. This way would me enable to do some analyses over longer time (note that Domotics will not keep detailed data for longer than a week).

## The heatpump-logger script

The script is desgned to run as a process in the background. On a linux system you can run it as a systemd service.

## Preparing / testing

1. Enable the webserver on your Alpha Innotec heatpump. I would suggest to look around on the web pages this webserver offers. These pages will be used to obtain the data for logging. So you can decide about what you would to log.
1. If you don't have an existing Domoticz service running, create one. I would recommend to run domoticz and the heatpump-logger on a raspberry pi for 24/7 logging.
1. `cp heatpump-logger-example.ini heatpump-logger.ini` and put the IP addresses of the heatpump and the domoticz server in place and give "test" the value "True" (!).
1. Check the `pages` dictionary in the `heatpump-logger.py` script. If the web interface of your heatpump is not in the Dutch language, you will at least have to replace the Duth labels. And maybe you prefer to make another selection of data for logging. Note that the numbering of the items start with "0", so the 6th item on a web page is specified with field number 5.
1. Create deviceIDs in Domoticz [see this](http://domoticx.com/internet-of-things-domoticz-data-ontvangen-vanuit-andere-bron/) for all data points and put the deviceID's in the `pages` dictionary of `heatpump-logger.py`.
1. Run the script and check the output.

## Installation

1. Copy heatpump-logger and heatpump.ini to the correct location (I use /home/pi). Make sure that in the .ini file "test" has the value "False", otherwise it can not run as a service.
1. Copy the heatpump-logger.service file to the correct directory (typically /etc/systemd/system/) and check working directory.
1. Run `systemctl enable --now heatpump-logger.service` to start the service.
