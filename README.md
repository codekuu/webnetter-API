<p align="center">
  <img src="https://i.imgur.com/SWoPeSe.png">
Plug and Play Network Management API built on Docker, fastAPI & Netmiko with optional GUI.
</p>

## Quick Links:
- [Description](#description)
- [Setup](#setup)
- [Settings](#settings)
- [Endpoints](#endpoints)
  - [Example Calls](#example-calls)
- [Contribute](contribute)

Live demos:
[:computer: GUI Enabled :computer:](https://oppetinternet.se/webnetter)
[:computer: Swagger Docs :computer:](https://oppetinternet.se/docs)


## Description

The goal of the Webnetter API is to make it a portable but also a static Network Management tool for any network.
Frontend/ GUI is optional in Webnetter API and built on Vue with Vuetify.
Repo for GUI/ Frontend can be found [HERE](https://github.com/codekuu/webnetter-API-FRONTEND).

API & Backend is built on fastAPI together with Netmiko.
FastAPI provides Swagger as documentation on endpoints at {url}/docs.
Everything is built inside docker which makes it scalable and easy to setup.

We aim towards easy-to-use and easy-to-setup.
Feel free to come up with ideas on how we can improve the service.

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
**Requirements:** Docker & Network connection.

    docker build -t webnetter-image .
    docker run --net=host -d --name webnetter-container -p 80:80 webnetter-image


## Settings
You can configure most of the main settings through the `config.py` file which is located in the main folder.

**FRONTEND GUI**
ENABLED as default, can be disabled.

**SWAGGER DOCS**
ENABLED as default, can be disabled.

**LOGFILE**
Logging requests made into a logfile with logging module, you can change filename and destination.

**BLACKLIST**
We provide a blacklist filter which every function looks through before making a request through netmiko.
Here you can add IP address of end-devices you would like to block, EMPTY as default.

## ENDPOINTS

Endpoint | Type | Description
--|--|--
/webnetter/ping/:host | GET | Ping Hostname/ IP
/webnetter/runcommands | POST | Send command to host, returning output.
/webnetter/configure | POST | Send file with configuration which netmiko will execute row by row, summary is sent by Webnetter API.
/webnetter/scp | POST | Send file to host through SCP, netmiko will verify and Webnetter will send the data back.

Responses from API follows specifications from https://github.com/omniti-labs/jsend.

## Example Calls



## **[GET]** ```/webnetter/ping/www.google.se```
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




## **[POST]** ```/webnetter/runcommands```
```javascript
"hosts": [
        {
          "host":"192.168.10.111",
          "username":"codekuu",
          "password":"TmljZSB0cnkgOyk=",
          "device_type":"hp_comware",
          "port":22,
          "command":"display interface brief"
        },
        {
          "host":"192.168.10.124",
          "username":"codekuu",
          "password":"TmljZSB0cnkgOyk=",
          "device_type":"linux",
          "port":22,
          "command":"pwd"
        }
]
```

Response:
```javascript
"status":"success"
"data":[
        {
          "success":true
          "software":"hp_comware",
          "host":"192.168.10.111",
          "output":"Brief information on interfaces in route mode:\nLink: ADM - administratively down; Stby - standby\nProtocol: (s) - spoofing\nInterface            Link Protocol Primary IP      Description                \nInLoop0              UP   UP(s)    --                                         \nNULL0                UP   UP(s)    --                                         \nVlan10               UP   UP       192.168.10.111                             \n\nBrief information on interfaces in bridge mode:\nLink: ADM - administratively down; Stby - standby\nSpeed: (a) - auto\nDuplex: (a)/A - auto; H - half; F - full\nType: A - access; T - trunk; H - hybrid\nInterface            Link Speed   Duplex Type PVID Description                \nGE1/0/1              UP   1G(a)   F(a)   T    10           UPLINK-192.168.10.1\nGE1/0/2              DOWN auto    A      A    1337                            \nGE1/0/3              DOWN auto    A      A    1337                            \nGE1/0/4              DOWN auto    A      A    1337                            \nGE1/0/5              DOWN auto    A      A    1337                            \nGE1/0/6              DOWN auto    A      A    1337                            \nGE1/0/7              DOWN auto    A      A    1337                            \nGE1/0/8              DOWN auto    A      A    1337                            \nGE1/0/9              DOWN auto    A      A    1337                            \nGE1/0/10             DOWN auto    A      A    1337                            \nGE1/0/11             DOWN auto    A      A    1337                            \nGE1/0/12             DOWN auto    A      A    1337                            \nGE1/0/13             DOWN auto    A      A    1337                            \nGE1/0/14             DOWN auto    A      A    1337                            \nGE1/0/15             DOWN auto    A      A    1337                            \nGE1/0/16             DOWN auto    A      A    1337                            \nGE1/0/17             DOWN auto    A      A    1337                            \nGE1/0/18             DOWN auto    A      A    1337                            \nGE1/0/19             DOWN auto    A      A    1337                            \nGE1/0/20             DOWN auto    A      A    1337                            \nGE1/0/21             DOWN auto    A      A    1337                            \nGE1/0/22             DOWN auto    A      A    1337                            \nGE1/0/23             DOWN auto    A      A    1337                            \nGE1/0/24             DOWN auto    A      A    1337                            \nXGE1/0/25            DOWN auto    A      A    1                               \nXGE1/0/26            DOWN auto    A      A    1                               \nXGE1/0/27            DOWN auto    A      A    1                               \nXGE1/0/28            DOWN auto    A      A    1                               \n",
      
        },
        {
          "success":true
          "software":"linux",
          "host":"192.168.10.124",
          "output":"/home/codekuu",
        }
]
```



## **[POST]** ```/webnetter/configure```
```javascript
Headers: {'Content-Type': 'multipart/form-data'}
Content-Disposition: form-data; name="file"; filename="test.txt"
Content-Type: text/plain:

sysname codekuu-test


Content-Disposition: form-data; name="hosts"

"hosts":[
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
"status":"success"
"data":[      
        {
          "success":true
          "software":"hp_comware",
          "host":"192.168.10.111",
          "output":"system-view\nSystem View: return to User View with Ctrl+Z.\n[codekuu-test]sysname codekuu-test\n[codekuu-test]return\n<codekuu-test>",
        },
        {
          "success":true
          "software":"hp_comware",
          "host":"192.168.10.112",
          "output":"system-view\nSystem View: return to User View with Ctrl+Z.\n[codekuu-test]sysname codekuu-test\n[codekuu-test]return\n<codekuu-test>",
        }
],

```



## **[POST]** ```/webnetter/scp```
```javascript
Headers: {'Content-Type': 'multipart/form-data'}
Content-Disposition: form-data; name="file"; filename="test.txt"
Content-Type: text/plain:

sysname test


Content-Disposition: form-data; name="hosts"

"hosts":[
          {
            "host": "192.168.10.112",
            "username": "codekuu"
            "password": "TmljZSB0cnkgOyk=",
            "device_type": "hp_comware",
            "port": 22
            "location": "/home/codekuu"
          }
]

```

Response:
```javascript
"status":"success"
"data":[
        {
          "success":false
          "software":"linux",
          "host":"192.168.10.124",
          "output":"Could not transfer file, it already exist in /home/pi.",
        }
]
```


## Contribute

**Do you have ideas?**
We are open for future development ideas, start an issue and tell us what you would like to have implemented.

**Found an error or want to help me write better code?**
We love critic, if you find something in the code that's bad or can be enhached please start an issue and we will respond you as fast as I can.

# We :dog: OPEN SOURCE
