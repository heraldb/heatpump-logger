# heatpump-logger
Logs data from Alpha Innotec heatpump to file and to Domoticz

## Introduction

Having a heatpump at work to warm your house is a great thing, but sometimes you might to have more insight in what is happening in this machine and why it operates the way it does. This logger can help you with that.

The script is set up to run on a Raspberry Pi, but you can run it on any machine with Python3.

The data points I have choosen to log can be different from what others may want to log. And that is easy to adapt in the script.

## Source of data

Data is obtained from a Alpha Innotec WZSV heatpump, using the web interface. You can check the user manual to find out how to start the webserver on the heatpump. The password you choose for the web insterface is not relevant for the heatpump-logger script, since it uses readonly access which is available without password.

## Output of data

Since I happened to run Domoticz already for my "Slimme meter" (common in the Netherlands to read data about usage of electricity and gas), it seamed a good idea to send the data Domoticz. In order to do this, you need to prepaire Domoticz for receiving data. I used this Dutch guide: http://domoticx.com/internet-of-things-domoticz-data-ontvangen-vanuit-andere-bron/](http://domoticx.com/internet-of-things-domoticz-data-ontvangen-vanuit-andere-bron/). Basically you need te create so called device numbers which can be used as a reference when you push data to Domoticz.

Apart from pushing data to Domoticz, I personally wanted to log the data to file as well, a 5 minute intervals. This way would me enable to do some analyses over longer time (note that Domotics will not keep detailed data for longer than a week.

## The heatpump-logger script

The script is desgned to run as a process in the background. On a linux system you can run it as a systemd service.
