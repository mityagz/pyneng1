import telnetlib
import time
from pprint import pprint
import re


def to_bytes(line):
    return f"{line}\n".encode("utf-8")

def pmpt(line):
    return ("\w+@\w+" + line).encode("utf-8")

def send_show_command(ip, username, password, enable, command, prompt='>'):
    with telnetlib.Telnet(ip) as telnet:
        telnet.read_until(b"login:")
        telnet.write(to_bytes(username))
        telnet.read_until(b"Password:")
        telnet.write(to_bytes(password))
        index, m, output = telnet.expect([ pmpt(prompt) ])
        """
        if index == 0:
            telnet.write(b"enable\n")
            telnet.read_until(b"Password")
            telnet.write(to_bytes(enable))
            telnet.read_until(b"#", timeout=5)
        """
        time.sleep(3)
        telnet.read_very_eager()

        telnet.write(to_bytes(command))
        result = ""

        while True:
            index, match, output = telnet.expect([ b"\-{3}\(more( \d{1,3}\%)?\)\-{3}", pmpt(prompt) ], timeout=5)
            output = output.decode("utf-8")
            #output = re.sub(" +--more--| +\x08+ +\x08+", "\n", output)
            result += output
            if index in (1, -1):
                break
            telnet.write(b" ")
            time.sleep(1)
            result.replace("\r\n", "\n")

        return result


if __name__ == "__main__":
    devices = [ "10.248.0.65", "10.248.0.66" ]
    for ip in devices:
        result = send_show_command(ip, "am", "qwerty", "cisco", "show conf")
        #pprint(result, width=120)
        print(result)
