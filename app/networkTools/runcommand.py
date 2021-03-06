#!/usr/bin/python3

# GENERAL IMPORTS
import os
import base64
import config
import traceback

# NETMIKO
from netmiko import ConnectHandler
from concurrent.futures import ProcessPoolExecutor, wait


def netmiko_runner(host):

    ###################
    # BACKEND
    blacklistHosts = os.path.join(config.blackListFile)  # Blacklist from config.py
    ############################
    # CHECK IF PASSWORD IS BASE64
    try:
        base64.b64encode(base64.b64decode(host["password"])) == host["password"]
    except Exception:
        return {
            "success": False,
            "host": host["host"],
            "software": host["device_type"],
            "output": "Password has to be encoded with base64 before process.",
        }

    with open(blacklistHosts, "r") as blacklist:

        try:
            if host["host"] not in blacklist.read():

                # CONNECTION DATA
                connectData = {
                    "device_type": host["device_type"],
                    "host": host["host"],
                    "username": host["username"],
                    "password": base64.b64decode(host["password"]).decode("ascii"),
                    "port": host["port"],
                }

                try:
                    # OPERATION
                    net_connect = ConnectHandler(**connectData)
                    response = net_connect.send_command(host["command"])
                    net_connect.disconnect()
                    return {
                        "success": True,
                        "host": host["host"],
                        "software": host["device_type"],
                        "output": response,
                    }

                except Exception as error_message:
                    info = str(error_message)
                    print(f"{host['host']} {info} {traceback.format_exc()}")
                    return {
                        "success": False,
                        "host": host["host"],
                        "software": host["device_type"],
                        "output": info,
                    }

            else:
                return {
                    "success": False,
                    "host": host["host"],
                    "software": host["device_type"],
                    "output": "Host blacklisted.",
                }

        except Exception as error_message:
            info = str(error_message)
            print(f"{host['host']} {info} {traceback.format_exc()}")
            return {
                "success": False,
                "host": host["host"],
                "software": host["device_type"],
                "output": info,
            }


class runcommand:
    def run(request, hosts):

        # Settings and standard Request Message
        responseData = []

        max_threads = 50
        pool = ProcessPoolExecutor(max_threads)
        future_list = []

        for host in hosts:
            future = pool.submit(netmiko_runner, host)
            future_list.append(future)

        wait(future_list)

        for return_data in future_list:
            responseData.append(return_data.result())

        return responseData
