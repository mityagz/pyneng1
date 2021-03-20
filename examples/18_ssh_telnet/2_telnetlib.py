import telnetlib
import time
from pprint import pprint


def to_bytes(line):
    return f"{line}\n".encode("utf-8")

def fpmpt(prompt):
    pmpt = ("\w+@\w+" + prompt).encode('utf-8')
    return pmpt


def send_show_command(ip, username, password, enable, commands, prompt=">"):
    pmpt = fpmpt(prompt)
    with telnetlib.Telnet(ip) as telnet:
        telnet.read_until(b"login:")
        telnet.write(to_bytes(username))
        telnet.read_until(b"Password:")
        telnet.write(to_bytes(password))
        index, m, output = telnet.expect([ pmpt ])
        """
        if index == 0:
            telnet.write(b"enable\n")
            telnet.read_until(b"Password")
            telnet.write(to_bytes(enable))
            telnet.read_until(b"#", timeout=5)
        """
        telnet.write(b"set cli screen-length 0\n")
        telnet.read_until(pmpt, timeout=5)
        time.sleep(3)
        telnet.read_very_eager()

        result = {}
        for command in commands:
            telnet.write(to_bytes(command))
            output = telnet.read_until(pmpt, timeout=5).decode("utf-8")
            result[command] = output.replace("\r\n", "\n")
        return result


if __name__ == "__main__":
    devices = [ "10.248.0.65" ]
    commands = ["show interface brief", "show arp"]
    for ip in devices:
        result = send_show_command(ip, "am", "qwerty", "cisco", commands)
        pprint(result, width=120)
