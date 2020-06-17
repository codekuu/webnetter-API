
# Webnetter API
Plug and Play Network Management API built on top of Netmiko with optional GUI.
Webnetter API is able to communicate and configure data on all types of machines.

## Quick Links:
- [Description](#description)
- [Setup](#setup)
- [Settings](#settings)
- [Endpoints](#endpoints)
- [Examples](#examples)
- [Contribute](contribute)

[:computer: Click here for Live demo :computer:](https://oppetinternet.se/webnetter)


## Description

Web GUI is built on VueJS with Vuetify (source for GUI is under frontend/).
API & Backend is built on Flask together with Netmiko.
The goal of the Webnetter API is to make it a portable but also a static Network Management tool for any network. We / I will develop more services for the Webnetter API. Feel free to come up with ideas on how we can improve the service.

Responses from API follows specifications from https://github.com/omniti-labs/jsend.

Webnetter-API is using Netmiko for communicating with platforms such as:
- Arista EOS
- Cisco ASA
- Cisco IOS/IOS-XE
- Cisco IOS-XR
- Cisco NX-OS
- Cisco SG300
- HP Comware7
- HP ProCurve
- Juniper Junos

See [Netmiko](https://github.com/ktbyers/netmiko) for all supported platforms and more. 

## Setup

    pip install --upgrade -r requirements.txt

**Start locally** (Standard: 0.0.0.0:5000)

    python webnetter.py

**Start server with WSGI**

    python webnetter.wsgi
 

## Settings
You can configure most of the main settings through the `settings.py` file which is located in the main folder.

 **TLS SSL**
  Disabled as default but you can add keys and enable it through `settings.py`.

**FRONTEND GUI**
Enabled as default, can be disabled.

**BACKEND HOST**
0.0.0.0 as default.

**LOGFILE**
We are logging every request made into a logfile, you can change filename and where to log.

**BLACKLIST**
We provide a blacklist filter which every function looks through before making a request through netmiko.
Here you can add IP address of anything you would like to block, people using it or machines you want to be out of reach. EMPTY as default.

## ENDPOINTS

Endpoint | Type | Description
--|--|--
/webnetter/ping/:host | GET | Ping Hostname/ IP
/webnetter/runcommand | POST | Send command to host, returning output.
/webnetter/configure | POST | Send file with configuration which netmiko will execute row by row, summary is sent by Webnetter API.
/webnetter/scp | POST | Send file to host through SCP, netmiko will verify and Webnetter will send the data back.


## Examples



**[GET]** /webnetter/ping/www.google.se
Response:
```javascript
{
    "status": "success",
    "data": {
        "host": "www.google.se",
        "up": true
    }
}
```




**[POST]** /webnetter/runcommand
```javascript
{
  "host": "192.168.10.111",
  "username": "codekuu",
  "password": "TmljZSB0cnkgOyk=",
  "device_type": "hp_comware",
  "port": 22,
  "command": "display interface brief"
}
```

Response:
```javascript
{
    "status": "success",
    "data": {
        "dataFromHost": "Brief information on interfaces in route mode:\nLink: ADM - administratively down; Stby - standby\nProtocol: (s) - spoofing\nInterface            Link Protocol Primary IP      Description                \nInLoop0              UP   UP(s)    --                                         \nNULL0                UP   UP(s)    --                                         \nVlan10               UP   UP       192.168.10.111                             \n\nBrief information on interfaces in bridge mode:\nLink: ADM - administratively down; Stby - standby\nSpeed: (a) - auto\nDuplex: (a)/A - auto; H - half; F - full\nType: A - access; T - trunk; H - hybrid\nInterface            Link Speed   Duplex Type PVID Description                \nGE1/0/1              UP   1G(a)   F(a)   T    10           UPLINK-192.168.10.1\nGE1/0/2              DOWN auto    A      A    1337                            \nGE1/0/3              DOWN auto    A      A    1337                            \nGE1/0/4              DOWN auto    A      A    1337                            \nGE1/0/5              DOWN auto    A      A    1337                            \nGE1/0/6              DOWN auto    A      A    1337                            \nGE1/0/7              DOWN auto    A      A    1337                            \nGE1/0/8              DOWN auto    A      A    1337                            \nGE1/0/9              DOWN auto    A      A    1337                            \nGE1/0/10             DOWN auto    A      A    1337                            \nGE1/0/11             DOWN auto    A      A    1337                            \nGE1/0/12             DOWN auto    A      A    1337                            \nGE1/0/13             DOWN auto    A      A    1337                            \nGE1/0/14             DOWN auto    A      A    1337                            \nGE1/0/15             DOWN auto    A      A    1337                            \nGE1/0/16             DOWN auto    A      A    1337                            \nGE1/0/17             DOWN auto    A      A    1337                            \nGE1/0/18             DOWN auto    A      A    1337                            \nGE1/0/19             DOWN auto    A      A    1337                            \nGE1/0/20             DOWN auto    A      A    1337                            \nGE1/0/21             DOWN auto    A      A    1337                            \nGE1/0/22             DOWN auto    A      A    1337                            \nGE1/0/23             DOWN auto    A      A    1337                            \nGE1/0/24             DOWN auto    A      A    1337                            \nXGE1/0/25            DOWN auto    A      A    1                               \nXGE1/0/26            DOWN auto    A      A    1                               \nXGE1/0/27            DOWN auto    A      A    1                               \nXGE1/0/28            DOWN auto    A      A    1                               \n"
    }
}
```



**[POST]** /webnetter/configure
```javascript
Headers: {'Content-Type': 'multipart/form-data'}
Content-Disposition: form-data; name="file"; filename="test.txt"
Content-Type: text/plain:

sysname test


Content-Disposition: form-data; name="hostData"

"hostData": [
              {
                "host": "192.168.10.111",
                "username": "codekuu",
                "password": "TmljZSB0cnkgOyk=",
                "device_type": "hp_comware",
                "port": 22
              },
              {
                "host": "192.168.10.112",
                "username": "codekuu",
                "password": "TmljZSB0cnkgOyk=",
                "device_type": "hp_comware",
                "port": 22
              }
            ]

```

Response:
```javascript
{
    "status":"success",
    "data": {
      "dataFromHost":"##### 192.168.10.111 #####\n\nsystem-view\nSystem View: return to User View with Ctrl+Z.\n[Great-Sysname]sysname test\nreturn\n<test>\n\n###########################\n\n##### 192.168.10.112 #####\n\nsystem-view\nSystem View: return to User View with Ctrl+Z.\n[Great-Sysname2]sysname test2\nreturn\n<test2>\n\n###########################\n\n"
    }
}

```



**[POST]** /webnetter/scp
```javascript
Headers: {'Content-Type': 'multipart/form-data'}
Content-Disposition: form-data; name="file"; filename="test.txt"
Content-Type: text/plain:

sysname test


Content-Disposition: form-data; name="hostData"

"hostData": [
              {
                "host": "192.168.10.111",
                "username": "codekuu",
                "password": "TmljZSB0cnkgOyk=",
                "device_type": "hp_comware",
                "port": 22
              },
              {
                "host": "192.168.10.124",
                "username": "codekuu",
                "password": "TmljZSB0cnkgOyk=",
                "device_type": "linux",
                "port": 22
              }
            ]

```

Response:
```javascript
{
    "status":"success",
    "data": {
      "dataFromHost":"##### 192.168.10.111 #####\n\ntest.txt was transferred and verified.\n\n###########################\n\n##### 192.168.10.124 #####\n\nCould not transfer file, it already exist in /home/pi/.\n\n###########################\n\n"
    }
}

```




## Contribute

**Do you have ideas?**
Im open for future development ideas, start an issue and tell me what you would like to have implemented.

**Found an error or want to help me write better code?**
I like critic, if you find something in my code that's bad or can be enhached please start an issue and I'll respond you as fast as I can.

# I :dog: OPEN SOURCE
