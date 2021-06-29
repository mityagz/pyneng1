# -*- coding: utf-8 -*-
"""
"""

data = {
    "PE0": {"mirroring_intf": None, "ri": "fnm-mirror-0", "mirrored_intf": "gr-0/0/10.1", "tun_src": "10.229.4.0", "tun_dst": "10.229.138.0", "tun_addr": "10.230.0.104"},
    "PE1": {"mirroring_intf": None, "ri": "fnm-mirror-0", "mirrored_intf": "gr-0/0/10.1", "tun_src": "10.229.132.0", "tun_dst": "10.229.138.0", "tun_addr": "10.230.0.106"},
    "PE2": {"mirroring_intf": None, "ri": "fnm-mirror-0", "mirrored_intf": "gr-0/0/10.1", "tun_src": "10.229.6.0", "tun_dst": "10.229.138.0", "tun_addr": "10.230.0.108"}, 
    "PE3": {"mirroring_intf": None, "ri": "fnm-mirror-0", "mirrored_intf": "gr-0/0/10.1", "tun_src": "10.229.134.0", "tun_dst": "10.229.138.0", "tun_addr": "10.230.0.110"},
    "SRX": {"mirrored_intf0": "gr-0/0/0.", 
            "mirrored_intf": "", 
           "ri": "fnm-mirror-0", 
           "mirror_out_intf": "", 
           "tun_src": "10.229.138.0",
           "tun_dst": "",
           "tun_addr": ""
           }
}

"""
cat templates/pe_mirror.txt templates/srx_mirror.txt 
PEs:

set chassis fpc 0 port-mirror-instance {{ ri }}
set interfaces {{ mirrored_intf }} family inet filter input {{ ri }}
set interfaces {{ mirrored_intf }} family inet filter output {{ ri }}
set interfaces {{ mirroring_intf }} tunnel source {{ tun_src }}
set interfaces {{ mirroring_intf }} tunnel destination {{ tun_dst }}
set interfaces {{ mirroring_intf }} family inet address {{ tun_addr }}
set forwarding-options port-mirroring instance {{ ri }} input rate 1
set forwarding-options port-mirroring instance {{ ri }} input run-length 0
set forwarding-options port-mirroring instance {{ ri }} family inet output next-hop-group {{ ri }}
set forwarding-options next-hop-group {{ ri }} group-type inet
set forwarding-options next-hop-group {{ ri }} interface {{ mirroring_intf }}
set firewall family inet filter {{ ri }} term {{ ri }} then port-mirror-instance {{ ri }}

SRX:

set security zones security-zone {{ ri }} interfaces {{ mirrored_intf }}
set interfaces {{ mirrored_intf }} tunnel source {{ tun_src }}
set interfaces {{ mirrored_intf }} tunnel destination {{ tun_dst }}
set interfaces {{ mirrored_intf }} family inet filter input {{ ri }}
set interfaces {{ mirrored_intf }} family inet address {{ tun_addr }}
"""

import sys
import yaml
from jinja2 import Environment, FileSystemLoader
import os
from task_20_1 import generate_config
from ncclient import manager
#import xmltodict, json

def get_id_gr(dev):
    return "gr-0/0/10.20"

def create_mirror_config(dev, tmpl, data):
    return(generate_config(tmpl, data))

def conf_mirror_pe(dev, conf):
    #print(dev['host'], dev['ip'], dev['username'], dev['password'])
    confList = conf.split("\n")
    if dev['host'] == PE:
     print(confList)
     s = manager.connect(host = dev['ip'], port = 22, username = dev['username'], password = dev['password'], hostkey_verify=False, device_params={'name':'junos'})
     s.lock()
     s.load_configuration(action='set', config=confList)
     s.commit()
     s.unlock()
    return conf

def conf_mirror_srx0(dev, conf):
    ip_srx = "10.229.138.0"
    confList = conf.split("\n")
    if dev['host'] == PE:
     print(confList)
     s = manager.connect(host = ip_srx, port = 22, username = dev['username'], password = dev['password'], hostkey_verify=False, device_params={'name':'junos'}, timeout=600)
     s.lock()
     s.load_configuration(action='set', config=confList)
     s.commit()
     s.unlock()
    return conf

def conf_mirror_pes(pes, pe_tmpl, sw_tmpl, data):
    rres_conf = ''
    for pe_dev in (pes):
        data[pe_dev['host']]['mirroring_intf'] = get_id_gr(pe_dev)
        pe_conf = create_mirror_config(pe_dev, pe_tmpl, data[pe_dev['host']])
        res_conf = conf_mirror_pe(pe_dev, pe_conf)
        rres_conf += res_conf + '\n-------------------------------------------------\n'
        #print(rres_conf)
    return rres_conf

def conf_mirror_srx(pes, pe_tmpl, sw_tmpl, data):
    rres_conf = ''
    unit = 20
    for pe_dev in (pes):
        data['SRX']['tun_dst'] = data[pe_dev['host']]['tun_src']
        (o0, o1, o2, o3) = (data[pe_dev['host']]['tun_addr']).split('.')
        data['SRX']['tun_addr'] = ".".join([o0, o1, o2, str(int(o3) + 1)])
        data['SRX']['mirrored_intf'] = data['SRX']['mirrored_intf0'] + str(unit) 
        pe_conf = create_mirror_config(pe_dev, sw_tmpl, data['SRX'])
        res_conf = conf_mirror_srx0(pe_dev, pe_conf)
        rres_conf += res_conf + '\n-------------------------------------------------\n'
        #print(data['SRX'])
        unit += 1
    return rres_conf

if __name__ == "__main__":
    PE = ''
    args = sys.argv[1:]
    if len(args) != 1:
        quit()
    PE = args[0]
    with open("devices0.yaml") as f:
        devices = yaml.safe_load(f)
    tmpl1 = "templates/pe_mirror.txt"
    tmpl2 = "templates/srx_mirror.txt"
    conf_mirror_pes(devices, tmpl1, tmpl2, data)
    conf_mirror_srx(devices, tmpl1, tmpl2, data)
