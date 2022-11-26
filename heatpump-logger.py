#!/usr/bin/python
import websocket
import json
from time import sleep
import xml.etree.ElementTree as ET
from datetime import datetime
import urllib.request
import sys
import os
import configparser

config = configparser.ConfigParser()
config.read('./heatpump-logger.ini')
heatpumpIP = config['NETWORK']['HEATPUMP_IP']
domoIP = config['NETWORK']['DOMOTICZ_IP']
INTERVAL = config['LOGGING'].getint('INTERVAL')
LOGFILE = config['LOGGING']['LOGFILE']
TEST = config['DEBUG'].getboolean('TEST')


def ft(v): return v[0:-2]   # strip ' °C'
def fp(v): return v[0:-3]   # strip ' KW'
def fe(v): return v[0:-4]   # strip ' KWh'
def fs(v): return v or 'Uit'
def times1000(v): return str(float(v)*1000)


pages = {
    # page_id: [[
    # 1. field number on page
    # 2. domo deviceID
    # 3. description on page
    # 4. formatter function
    # 5. conversion for domoticz push] ....]
    'temp': [
        [0, 14, "Aanvoer",  ft, None],
        [1, 15, "Retour",  ft, None],
        [2, 16, "Retour berekend",  ft, None],
        [4, 17, "Buitentemperatuur",  ft, None],
        [5, 18, "Tapwater gemeten",  ft, None],
        [7, 19, "Bron-in",  ft, None],
        [8, 20, "Bron-uit",  ft, None],
    ],
    'status': [
        [5, 12, "Bedrijfstoestand", fs, None],
        [6, 23, "Vermogen", fp, times1000]
    ],
    'energy': [
        [0, None, "Verwarmen", fe, times1000],
        [1, None, "Warmwater", fe, times1000],
    ]
}


def push(domoID, value):
    if TEST:
        print(f"pushing {value} to device {domoID}")
    else:
        try:
            url = (f"http://{domoIP}/json.htm?type=command&param=udevice&"
                   f"idx={domoID}&nvalue=0&svalue={value}")
            result = urllib.request.urlopen(url, timeout=1)
            # print(result.getcode())
        except:
            print(sys.exc_info())


def parseNavigation(xml):
    root = ET.fromstring(xml)
    items = root[0].findall('item')
    item_temp = items[0]
    item_status = items[7]
    item_energy = items[8]
    if item_temp[0].text != "Temperaturen" or \
            item_status[0].text != "Installatiestatus" or \
            item_energy[0].text != "Energie":
        raise Exception("Menuitems changed?")

    return (item_temp.attrib['id'],
            item_status.attrib['id'],
            item_energy.attrib['id'])


def parse_items(root, page):
    items = root.findall('item')
    values = []
    for (n, domoID, label, fmt, fpush) in page:
        item = items[n]
        text = item[0].text
        if text != label:
            raise Exception(
                f"found {text} instead of {label} on position {n}")
        value = fmt(item[1].text) if fmt else item[1].text
        if domoID:
            push(domoID, fpush(value) if fpush else value)
        values.append(value)
    return values


def parse_page(menu_id, page):
    ws.send(f'GET;{menu_id}')
    root = ET.fromstring(ws.recv())
    return parse_items(root, page)


def log(now, values):
    s = f'{str(now)[0:-7]} {" ".join(values)}\n'
    if TEST:
        print(s, end='')
    elif LOGFILE:
        with open(LOGFILE, "a") as f:
            f.write(s)


ws = websocket.WebSocket()
ws.connect(f"ws://{heatpumpIP}:8214", subprotocols=["Lux_WS"])
ws.send(f'LOGIN;')  # we don't need a password to obtain the data

result = ws.recv()
(menu_temp_id, menu_status_id, menu_energy_id) = parseNavigation(result)

now = datetime.now()
last_print = -1
while True:
    if TEST or (now.minute % 5 == 0 and last_print != now.minute):
        doprint = True
        last_print = now.minute
    else:
        doprint = False

    values = parse_page(menu_status_id, pages['status'])
    values += parse_page(menu_temp_id, pages['temp'])
    if doprint:
        values += parse_page(menu_energy_id, pages['energy'])
        log(now, values)

    if TEST:
        break

    sleep(INTERVAL)
    now = datetime.now()
