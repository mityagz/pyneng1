import pexpect
import re
from pprint import pprint


def send_show_command(ip, username, password, enable, command, prompt=">"):
    with pexpect.spawn(f"ssh {username}@{ip}", timeout=10, encoding="utf-8") as ssh:
        ssh.expect("[Pp]assword")
        ssh.sendline(password)
        """
        enable_status = ssh.expect([">", "#"])
        if enable_status == 0:
            ssh.sendline("enable")
            ssh.expect("[Pp]assword")
            ssh.sendline(enable)
            ssh.expect(prompt)
        """
        prompt = "\w+\@\w+" + prompt
        ssh.expect(prompt)
        ssh.sendline(command)
        output = ""

        while True:
          try:
            match = ssh.expect([prompt, '\-{3}\(more( \d{1,3}\%)?\)\-{3}', pexpect.TIMEOUT])
            page = ssh.before
            page = ssh.before.replace("\r\n", "\n")
            page = re.sub(" +\x08+ +\x08+", "\n", page)
            output += page
            if match == 0:
                break
            elif match == 1:
                #print(str(ssh))
                ssh.send(" ")
            else:
                print("Ошибка: timeout")
                break
          except:
                print(str(ssh))
        output = re.sub("\n +\n", "\n", output)
        return output


if __name__ == "__main__":
    devices = ["10.248.0.65", "10.248.0.66"]
    for ip in devices:
        result = send_show_command(ip, "am", "qwerty", "cisco", "show configuration")
        with open(f"{ip}_result.txt", "w") as f:
            f.write(result)
