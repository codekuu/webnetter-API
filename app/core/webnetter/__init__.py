import os
import base64
from configuration import logger
from netmiko import ConnectHandler, file_transfer
from concurrent.futures import ProcessPoolExecutor, wait


def return_object(
    success: bool = False, host: str = "", software: str = "", output: str = ""
):
    """
    Return a dictionary with the following structure:
    {
        "success": bool,
        "host": str,
        "software": str,
        "output": str
    }
    """
    return {
        "success": success,
        "host": host,
        "software": software,
        "output": output,
    }


def netmiko_runner(
    host: dict = {},
    run_type: str = "",
    configuration_set: list = [],
    scp_file_path: str = "",
    file_name: str = "",
):
    """
    This function is used to run commands on a remote device.
    :param host: The host to connect to.
    :param run_type: The type of run to perform.
    :param configuration_set: The configuration set to use.
    :param scp_file_path: The path to the file to transfer.
    :return: A dictionary containing the results of the run.
    """
    try:
        # CHECK THAT ALL KEYS ARE IN DATA
        if not all(
            key in host
            for key in (
                "username",
                "password",
                "device_type",
                "port",
                "host",
            )
        ):
            return return_object(
                False,
                host.get("host", "Unknown"),
                host.get("device_type", "Unknown"),
                "Missing data in request.",
            )

        connectData = {
            "device_type": host["device_type"],
            "host": host["host"],
            "username": host["username"],
            "password": base64.b64decode(host["password"]).decode("ascii"),
            "port": host["port"],
        }

        net_connect = ConnectHandler(**connectData)
        if run_type == "configure":
            response = net_connect.send_config_set(
                config_commands=configuration_set, cmd_verify=False
            )
        elif run_type == "runcommand":
            response = net_connect.send_command(host["command"])
        elif run_type == "scp":
            response = file_transfer(
                net_connect,
                source_file=scp_file_path,
                dest_file=file_name,
                file_system=host["location"],
                direction="put",
                overwrite_file=False,
            )
            if not response["file_verified"]:
                response = "We could not verify the transfer, check manually."

            response = f"{file_name} was transferred and verified."
        else:
            raise Exception("Missing run_type")
        net_connect.disconnect()

        return return_object(True, host["host"], host["device_type"], response)

    except Exception as error_message:
        logger.warning(f"Webnetter.scp:{error_message}")
        return return_object(
            False,
            host.get("host", "Unknown"),
            host.get("device_type", "Unknown"),
            "Failed to carry out operation, read logs for more information.",
        )


class Webnetter:
    def __init__(self, max_threads: int = 50, hosts: list = []):
        """
        Initialize the class.
        """
        self.pool = ProcessPoolExecutor(max_threads)
        self.hosts = hosts
        self.response_data = []
        self.future_list = []

    def runcommand(self):
        """
        Run a command on a remote device.
        """
        for host in self.hosts:
            future = self.pool.submit(netmiko_runner, host, "runcommand")
            self.future_list.append(future)

        wait(self.future_list)

        for return_data in self.future_list:
            self.response_data.append(return_data.result())

        return self.response_data

    async def configure(self, config_file):
        """
        Configure a remote device.
        """
        config_file = await config_file.read()
        configuration_set = config_file.decode("utf-8").split("\n")
        if not configuration_set:
            raise Exception("Error when parsing configuration file.")

        for host in self.hosts:
            future = self.pool.submit(
                netmiko_runner, host, "configure", configuration_set
            )
            self.future_list.append(future)

        wait(self.future_list)

        for return_data in self.future_list:
            self.response_data.append(return_data.result())

        return self.response_data

    async def scp(self, scp_file):
        """
        SCP a file to a remote device.
        """
        savePath = os.path.dirname(__file__) + scp_file.filename
        confugrationFileContent = await scp_file.read()
        confugrationFileContent = confugrationFileContent.decode("utf-8")
        if confugrationFileContent == "":
            raise Exception("No configuration file found.")

        with open(savePath, "w") as temp_file:
            temp_file.write(confugrationFileContent)

        for host in self.hosts:
            future = self.pool.submit(
                netmiko_runner, host, "scp", None, savePath, scp_file.filename
            )
            self.future_list.append(future)

        wait(self.future_list)

        for return_data in self.future_list:
            self.response_data.append(return_data.result())

        if savePath:
            os.remove(savePath)

        return self.response_data
