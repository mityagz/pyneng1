from pprint import pprint
import yaml
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)


def send_show_command(device, commands):
    result = {}
    try:
        with ConnectHandler(**device) as ssh:
            #ssh.enable()
            for command in commands:
                output = ssh.send_command(command)
                result[command] = output
        return result
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        print(error)


if __name__ == "__main__":
    device = {
        "device_type": "juniper_junos_telnet",
        "ip": "10.248.0.65",
        "username": "am",
        "password": "qwerty",
        "secret": "cisco",
    }
    result = send_show_command(device, ["show system uptime", "show arp"])
    pprint(result, width=120)
