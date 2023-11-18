<h1>Archived</h1>
<h2>Webnetter-API has been archived.<h2/>

<p align="center">
  <img src="https://i.imgur.com/SWoPeSe.png">
Plug and Play Network Management API built on Docker, fastAPI & Netmiko with GUI.
</p>

## Quick Links:
- [Description](#description)
- [Setup](#setup)
- [Settings](#settings)
- [Endpoints](#endpoints)
  - [Example Calls](#example-calls)
- [Contribute](contribute)


## Description

The goal of the Webnetter API is to make it a portable but also a static Network Management tool for any network.
Webnetter API comes with a frontend built on VueJS with Vuetify.

API & Backend is built on fastAPI together with Netmiko.
FastAPI provides Swagger as documentation on endpoints at {url}/docs.
Everything is built inside docker which makes it scalable and easy to setup.

We aim towards easy-to-use and easy-to-setup.
Feel free to come up with ideas on how webnetter can improve the service.

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
- Linux *

See [Netmiko](https://github.com/ktbyers/netmiko) for all supported platforms and more. 

## Setup
**Requirements:** Docker & Network connection.

**Docker**
```bash
docker build -t webnetter-image .
docker run --net=host -d --name webnetter-container -p 80:80 webnetter-image
```
**Docker-compose**
```bash
docker-compose build
docker-compose up -d
```
(fyi, you might need sudo)

## Logs
Logs will be saved to a file called webnetter.log.


## ENDPOINTS

Endpoint | Type | Description
--|--|--
/webnetter/runcommands | POST | Send command to host, returning output.
/webnetter/configure | POST | Send file with configuration which netmiko will execute row by row, summary is sent by Webnetter API.
/webnetter/scp | POST | Send file to host through SCP, netmiko will verify and Webnetter will send the data back.

## Example Calls

## **[POST]** ```/webnetter/runcommands```
```json
{
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
}
```

Response:
```json
{
  "status":"success",
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
}
```



## **[POST]** ```/webnetter/configure```
```text
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
```json
{
  "status":"success",
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
  ]
}

```



## **[POST]** ```/webnetter/scp```
```text
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
```json
{
  "status":"success",
  "data":[
          {
            "success":false
            "software":"linux",
            "host":"192.168.10.124",
            "output":"Could not transfer file, it already exist in /home/pi.",
          }
  ]
}
```
