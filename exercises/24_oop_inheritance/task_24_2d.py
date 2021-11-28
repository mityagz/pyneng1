# -*- coding: utf-8 -*-

"""
Задание 24.2d

Скопировать класс MyNetmiko из задания 24.2c или задания 24.2b.

Добавить параметр ignore_errors в метод send_config_set.
Если передано истинное значение, не надо выполнять проверку на ошибки и метод должен работать точно так же как метод send_config_set в netmiko.
Если значение ложное, ошибки должны проверяться.

По умолчанию ошибки должны игнорироваться.


In [2]: from task_24_2d import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [6]: r1.send_config_set('lo')
Out[6]: 'config term\nEnter configuration commands, one per line.  End with CNTL/Z.\nR1(config)#lo\n% Incomplete command.\n\nR1(config)#end\nR1#'

In [7]: r1.send_config_set('lo', ignore_errors=True)
Out[7]: 'config term\nEnter configuration commands, one per line.  End with CNTL/Z.\nR1(config)#lo\n% Incomplete command.\n\nR1(config)#end\nR1#'

In [8]: r1.send_config_set('lo', ignore_errors=False)
---------------------------------------------------------------------------
ErrorInCommand                            Traceback (most recent call last)
<ipython-input-8-704f2e8d1886> in <module>()
----> 1 r1.send_config_set('lo', ignore_errors=False)

...
ErrorInCommand: При выполнении команды "lo" на устройстве 192.168.100.1 возникла ошибка "Incomplete command."
"""

class ErrorInCommand(Exception):
    """
    Исключение генерируется, если при выполнении команды на оборудовании, возникла ошибка.
    """

from netmiko.cisco.cisco_ios import CiscoIosSSH
import re


device_params = {
    "device_type": "cisco_ios",
    "ip": "10.229.10.0",
    "username": "am",
    "password": "qwerty",
    "secret": "cisco",
}



class MyNetmiko(CiscoIosSSH):
    #def __init__(self, device_type, ip, username, password, secret, disable_paging = True):
    def __init__(self, **device_params):
        self.dev_ip = device_params['ip']
        super().__init__(**device_params)
        self.enable()


    def _check_error_in_command(self, cmd, ocmd):
            regex = None
            err = r'% (?P<err>.*)'
            regex = re.search(err, ocmd)
            if regex:
                excn = "При выполнении команды \"{}\" на устройстве {} возникла ошибка {}".format(cmd, self.dev_ip, regex.group('err'))
                raise ErrorInCommand(excn)

    def send_command(self, cmd):
        ocmd = super().send_command(cmd)
        if cmd == 'logging':
            ocmd = super().send_config_set(cmd)
        self._check_error_in_command(cmd, ocmd)
        return ocmd

    def send_config_set(self, cmd, ignore_errors = True):
        ocmd = super().send_config_set(cmd)
        if not ignore_errors:
            self._check_error_in_command(cmd, ocmd)
        return ocmd

if __name__ == '__main__':
    r = MyNetmiko(**device_params)
    print(r.send_command('sh ip int br'))
    print(r.send_command('sh ip br'))


"""
python@debian: $  [master|✚ 15…73] 
21:00 $ pyneng 2d
======================================================================== test session starts =========================================================================
platform linux -- Python 3.8.2, pytest-6.2.1, py-1.10.0, pluggy-0.13.1 -- /home/python/venv/pyneng1/bin/python3.8
cachedir: .pytest_cache
metadata: {'Python': '3.8.2', 'Platform': 'Linux-4.9.0-9-amd64-x86_64-with-glibc2.17', 'Packages': {'pytest': '6.2.1', 'py': '1.10.0', 'pluggy': '0.13.1'}, 'Plugins': {'json-report': '1.2.4', 'metadata': '1.11.0', 'clarity': '0.3.0a0'}, 'GIT_BRANCH': 'master'}
rootdir: /home/python/pyneng1/exercises/24_oop_inheritance, configfile: pytest.ini
plugins: json-report-1.2.4, metadata-1.11.0, clarity-0.3.0a0
collected 8 items                                                                                                                                                    

test_task_24_2d.py::test_class_created PASSED                                                                                                                  [ 12%]
test_task_24_2d.py::test_class_inheritance PASSED                                                                                                              [ 25%]
test_task_24_2d.py::test_errors_ignore_false[Invalid input detected-logging 0255.255.1] PASSED                                                                 [ 37%]
test_task_24_2d.py::test_errors_ignore_false[Incomplete command-lo] PASSED                                                                                     [ 50%]
test_task_24_2d.py::test_errors_ignore_false[Ambiguous command-a] PASSED                                                                                       [ 62%]
test_task_24_2d.py::test_errors_ignore_true[Invalid input detected-logging 0255.255.1] PASSED                                                                  [ 75%]
test_task_24_2d.py::test_errors_ignore_true[Incomplete command-lo] PASSED                                                                                      [ 87%]
test_task_24_2d.py::test_errors_ignore_true[Ambiguous command-a] PASSED                                                                                        [100%]

---------------------------------------------------------------------------- JSON report -----------------------------------------------------------------------------
no JSON report written.
=================================================================== 8 passed, 1 warning in 54.01s ====================================================================
(pyneng1) 

"""
